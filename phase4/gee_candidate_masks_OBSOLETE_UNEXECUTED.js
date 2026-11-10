/*
PHASE 4: PREPARED, UNEXECUTED. Candidate Sentinel-1 backscatter change only.
Use the full CSV from gee_scene_inventory_UNEXECUTED.js first. Select exact
scene IDs after checking acquisition dates, matching relative orbit, pass,
mode, polarization, incidence angle and valid AOI coverage. NRSC observed
flooding 16 July 2018, so a July scene is never assumed dry by default.
No source-independent flood labels are embedded. Do not call any candidate
mask validated inundation or estimate affected rice area from it.
*/
var aoi = ee.Geometry.Rectangle([76.35, 9.45, 76.60, 9.75], null, false);
var SELECTED_ORBIT = null;  // Relative orbit number from full inventory.
var PASS = 'ASCENDING';     // Change if selected scenes are all DESCENDING.
var PRE_IDS = [];           // At least 2 individually reviewed pre-event scenes.
var EVENT_IDS = [];         // At least 2 scene IDs within a defined 2018 event interval.
var BASELINE_REVIEWED = false; // True only with dated evidence for each PRE scene.
var START_EXPORTS = false;     // Start only after inventory and QA review.
var ALLOW_SINGLE_SCENE = false;// Set true only with explicit documented limitation.
var MIN_SCENE_AOI_COVERAGE = 0.80;
var MAX_GROUP_MEAN_ANGLE_DIFF_DEG = 2;

Map.centerObject(aoi, 11);
Map.addLayer(aoi, {color:'yellow'}, 'Pilot AOI');
print('Configured pre/event IDs', PRE_IDS, EVENT_IDS);
if (SELECTED_ORBIT !== null && PRE_IDS.length && EVENT_IDS.length) {
  var collection = ee.ImageCollection('COPERNICUS/S1_GRD')
    .filterBounds(aoi)
    .filter(ee.Filter.eq('instrumentMode', 'IW'))
    .filter(ee.Filter.eq('orbitProperties_pass', PASS))
    .filter(ee.Filter.eq('relativeOrbitNumber_start', SELECTED_ORBIT))
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'));
  var pre = collection.filter(ee.Filter.inList('system:index', PRE_IDS)).sort('system:time_start');
  var event = collection.filter(ee.Filter.inList('system:index', EVENT_IDS)).sort('system:time_start');

  function metadata(col, role) {
    return ee.FeatureCollection(col.toList(col.size()).map(function(item) {
      var image = ee.Image(item);
      var valid = image.select('VV').mask().unmask(0,false).reduceRegion({
        reducer:ee.Reducer.mean(),geometry:aoi,scale:30,maxPixels:1e8,bestEffort:true}).get('VV');
      var angle = image.select('angle').reduceRegion({reducer:ee.Reducer.mean(),
        geometry:aoi,scale:1000,maxPixels:1e8,bestEffort:true}).get('angle');
      return ee.Feature(null, {
        role:role, scene_id:image.get('system:index'),
        acquisition_utc:ee.Date(image.get('system:time_start')).format('YYYY-MM-dd HH:mm:ss'),
        relative_orbit:image.get('relativeOrbitNumber_start'),
        absolute_orbit:image.get('orbitNumber_start'),
        pass_direction:image.get('orbitProperties_pass'),
        instrument_mode:image.get('instrumentMode'),
        polarizations:ee.List(image.get('transmitterReceiverPolarisation')).join('|'),
        vv_valid_fraction_of_aoi_approx_30m:valid,
        mean_incidence_angle_deg_approx:angle
      });
    }));
  }
  print('Exact selected scene metadata; check every row',
    metadata(pre,'reviewed_pre'), metadata(event,'event'));
  print('Matching scene counts; must equal configured ID lengths',pre.size(),event.size());

  var preVV = pre.select('VV');
  var eventVV = event.select('VV');
  var preMedian = preVV.median().rename('pre_median_vv_db');
  var eventMedian = eventVV.median().rename('event_median_vv_db');
  var preFirst = ee.Image(preVV.first()).rename('pre_first_vv_db');
  var eventMin = eventVV.min().rename('event_min_vv_db');
  var preCount = preVV.count().unmask(0,false).rename('pre_valid_scene_count');
  var eventCount = eventVV.count().unmask(0,false).rename('event_valid_scene_count');
  var overlap = preCount.gt(0).and(eventCount.gt(0)).rename('valid_overlap');
  var preAngle = pre.select('angle').mean().rename('pre_angle_mean_deg');
  var eventAngle = event.select('angle').mean().rename('event_angle_mean_deg');
  var angleDifference = preAngle.subtract(eventAngle).abs().rename('angle_abs_diff_deg');
  var drop = preMedian.subtract(eventMedian).rename('vv_drop_db');
  var firstDrop = preFirst.subtract(eventMedian).rename('vv_drop_pre_first_db');
  var minDrop = preMedian.subtract(eventMin).rename('vv_drop_event_min_db');

  // Only 2014–17 JRC annual water classes are used; the all-years 1984–2021
  // occurrence layer would include post-2018 observations in a 2018 baseline.
  var historic = ee.ImageCollection('JRC/GSW1_4/YearlyHistory')
    .filter(ee.Filter.gte('year',2014)).filter(ee.Filter.lte('year',2017))
    .select('waterClass');
  var validWaterYears = historic.map(function(img) {return img.gt(0);})
    .sum().rename('water_valid_years_2014_17');
  var permanentYears = historic.map(function(img) {return img.eq(3);})
    .sum().rename('water_permanent_years_2014_17');
  var waterKnown = validWaterYears.gte(3).rename('water_baseline_known');
  var nonPermanent = permanentYears.lt(3).rename('not_permanent_3_of_4_years');
  var slope = ee.Terrain.slope(ee.Image('USGS/SRTMGL1_003')).rename('slope_deg');
  var lowSlope = slope.lt(5).rename('slope_below_5deg');
  var strictValid = overlap.and(waterKnown).and(nonPermanent).and(lowSlope)
    .rename('strict_analysis_valid');
  var noWaterExclusionValid = overlap.and(lowSlope)
    .rename('valid_without_water_exclusion');
  function candidate(dbImage, eventImage, threshold, mask, name) {
    return dbImage.gte(threshold).and(eventImage.lt(-15))
      .updateMask(mask).rename(name).toByte();
  }
  var c2 = candidate(drop,eventMedian,2,strictValid,'candidate_2db');
  var c3 = candidate(drop,eventMedian,3,strictValid,'candidate_3db');
  var c4 = candidate(drop,eventMedian,4,strictValid,'candidate_4db');
  var preFirstC3 = candidate(firstDrop,eventMedian,3,strictValid,
    'candidate_3db_first_pre_scene');
  var eventMinC3 = candidate(minDrop,eventMin,3,strictValid,
    'candidate_3db_min_event_scene');
  var noWaterC3 = candidate(drop,eventMedian,3,noWaterExclusionValid,
    'candidate_3db_without_water_exclusion');
  Map.addLayer(preMedian,{min:-25,max:0},'Pre VV median');
  Map.addLayer(eventMedian,{min:-25,max:0},'Event VV median');
  Map.addLayer(c3.selfMask(),{palette:['#087fae']},'Candidate 3 dB, not validated');
  Map.addLayer(strictValid.selfMask(),{palette:['#6baf70']},'Valid comparison support',false);

  var guard = ee.Dictionary({
    pre_count:pre.size(), event_count:event.size(),
    pre_orbit_count:ee.List(pre.aggregate_array('relativeOrbitNumber_start')).distinct().size(),
    event_orbit_count:ee.List(event.aggregate_array('relativeOrbitNumber_start')).distinct().size(),
    historic_water_year_count:historic.size(),
    minimum_selected_scene_aoi_valid_fraction:metadata(pre,'reviewed_pre')
      .merge(metadata(event,'event')).aggregate_min('vv_valid_fraction_of_aoi_approx_30m'),
    pre_mean_angle_deg:metadata(pre,'reviewed_pre')
      .aggregate_mean('mean_incidence_angle_deg_approx'),
    event_mean_angle_deg:metadata(event,'event')
      .aggregate_mean('mean_incidence_angle_deg_approx')
  });
  print('Export guards',guard);
  if (START_EXPORTS) {
    if (!BASELINE_REVIEWED) throw new Error('Review every PRE scene for 2018 flooding first.');
    if (!ALLOW_SINGLE_SCENE && (PRE_IDS.length < 2 || EVENT_IDS.length < 2))
      throw new Error('Select at least two scenes in each group or document single-scene limitation.');
    var checks = guard.getInfo();
    if (checks.pre_count !== PRE_IDS.length || checks.event_count !== EVENT_IDS.length ||
        checks.pre_orbit_count !== 1 || checks.event_orbit_count !== 1 ||
        checks.historic_water_year_count !== 4 ||
        checks.minimum_selected_scene_aoi_valid_fraction === null ||
        checks.minimum_selected_scene_aoi_valid_fraction < MIN_SCENE_AOI_COVERAGE ||
        checks.pre_mean_angle_deg === null || checks.event_mean_angle_deg === null ||
        Math.abs(checks.pre_mean_angle_deg-checks.event_mean_angle_deg) >
          MAX_GROUP_MEAN_ANGLE_DIFF_DEG)
      throw new Error('Scene selection or water-history validation failed; no export.');
    var output = preMedian.addBands(eventMedian).addBands(preFirst).addBands(eventMin)
      .addBands(drop).addBands(firstDrop).addBands(minDrop)
      .addBands(preAngle).addBands(eventAngle).addBands(angleDifference)
      .addBands(preCount).addBands(eventCount).addBands(overlap)
      .addBands(validWaterYears).addBands(permanentYears).addBands(waterKnown)
      .addBands(nonPermanent).addBands(slope).addBands(lowSlope)
      .addBands(strictValid).addBands(noWaterExclusionValid)
      .addBands(c2).addBands(c3).addBands(c4)
      .addBands(preFirstC3).addBands(eventMinC3).addBands(noWaterC3);
    Export.image.toDrive({image:output,
      description:'phase4_kerala_2018_s1_pilot_candidate_bands_and_qa',
      region:aoi,scale:30,crs:'EPSG:32643',maxPixels:1e9,fileFormat:'GeoTIFF'});
    Export.table.toDrive({collection:metadata(pre,'reviewed_pre')
      .merge(metadata(event,'event')),
      description:'phase4_kerala_2018_s1_selected_scene_metadata',fileFormat:'CSV'});
  }
}
