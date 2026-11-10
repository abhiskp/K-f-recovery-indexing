/* Phase 4 exploratory S1 comparison, unexecuted template.
 * The inventory identifies two adjacent granules per selected acquisition.
 * Mosaic them BEFORE comparing dates. Reference dates precede NRSC's first
 * 16 July flood map, but their dry status is unverified. These bands and
 * masks are candidates, not validated inundation.
 */
var aoi = ee.Geometry.Rectangle([76.35,9.45,76.60,9.75],null,false);
var DATES = ['2018-06-10','2018-06-22','2018-07-04',
             '2018-07-16','2018-08-09','2018-08-21'];
var START_EXPORTS = true; // exact executed Code Editor version
var EXPORT_QA_TABLE = false; // table already completed in first run
var scenes = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(aoi)
  .filter(ee.Filter.eq('instrumentMode','IW'))
  .filter(ee.Filter.eq('platform_number','A'))
  .filter(ee.Filter.eq('orbitProperties_pass','DESCENDING'))
  .filter(ee.Filter.eq('relativeOrbitNumber_start',165))
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation','VV'));
function dayScenes(date) {
  var start=ee.Date(date);
  return scenes.filterDate(start,start.advance(1,'day')).sort('system:time_start');
}
function acquisition(date) {
  return dayScenes(date).select(['VV','angle']).mosaic().clip(aoi)
    .set('date_utc',date).set('system:time_start',ee.Date(date).millis());
}
var acq={};
DATES.forEach(function(date){acq[date]=acquisition(date);});
var acquisitionQA=ee.FeatureCollection(DATES.map(function(date){
  var col=dayScenes(date), image=acq[date];
  var valid=image.select('VV').mask().unmask(0,false).reduceRegion({
    reducer:ee.Reducer.mean(),geometry:aoi,scale:30,maxPixels:1e8,
    bestEffort:true}).get('VV');
  var angle=image.select('angle').reduceRegion({
    reducer:ee.Reducer.mean(),geometry:aoi,scale:1000,maxPixels:1e8,
    bestEffort:true}).get('angle');
  return ee.Feature(null,{date_utc:date,scene_count:col.size(),
    scene_ids:ee.List(col.aggregate_array('system:index')).join('|'),
    absolute_orbits:ee.List(col.aggregate_array('orbitNumber_start'))
      .distinct().join('|'),
    mosaic_valid_fraction_aoi_approx_30m:valid,
    mean_incidence_angle_deg_approx:angle,
    dry_status:'unverified',flood_label_status:'unvalidated'});
}));
print('Selected acquisition QA',acquisitionQA);
function medianBand(dates,band,name) {
  return ee.ImageCollection.fromImages(dates.map(function(d){
    return acq[d].select(band);
  })).median().rename(name);
}
var preEarly=medianBand(['2018-06-10','2018-06-22'],'VV','pre_early_vv_db');
var preLate=medianBand(['2018-06-22','2018-07-04'],'VV','pre_late_vv_db');
var preEarlyAngle=medianBand(['2018-06-10','2018-06-22'],
  'angle','pre_early_angle_deg');
var preLateAngle=medianBand(['2018-06-22','2018-07-04'],
  'angle','pre_late_angle_deg');
// Pre-2018 water history only. Class 0=no data, 3=permanent.
var historic=ee.ImageCollection('JRC/GSW1_4/YearlyHistory')
  .filter(ee.Filter.gte('year',2014))
  .filter(ee.Filter.lte('year',2017)).select('waterClass');
var waterValid=historic.map(function(i){return i.gt(0);}).sum()
  .rename('water_valid_years_2014_17');
var permanent=historic.map(function(i){return i.eq(3);}).sum()
  .rename('water_permanent_years_2014_17');
var waterKnown=waterValid.gte(3).rename('water_history_known');
var nonPermanent=permanent.lt(3).rename('not_permanent_3_of_4_years');
var slope=ee.Terrain.slope(ee.Image('USGS/SRTMGL1_003'))
  .rename('slope_deg');
var lowSlope=slope.lt(5).rename('slope_below_5deg');
function eventBands(date,prefix) {
  var event=acq[date].select('VV').rename(prefix+'_vv_db');
  var angle=acq[date].select('angle').rename(prefix+'_angle_deg');
  var valid=event.mask().unmask(0,false).rename(prefix+'_valid').toByte();
  var earlyOverlap=preEarly.mask().unmask(0,false).and(valid)
    .rename(prefix+'_early_overlap').toByte();
  var lateOverlap=preLate.mask().unmask(0,false).and(valid)
    .rename(prefix+'_late_overlap').toByte();
  var earlyQA=earlyOverlap.and(waterKnown).and(nonPermanent)
    .and(lowSlope).rename(prefix+'_early_strict_qa').toByte();
  var lateQA=lateOverlap.and(waterKnown).and(nonPermanent)
    .and(lowSlope).rename(prefix+'_late_strict_qa').toByte();
  var earlyDrop=preEarly.subtract(event).rename(prefix+'_early_drop_db');
  var lateDrop=preLate.subtract(event).rename(prefix+'_late_drop_db');
  function mask(drop,threshold,qa,name) {
    return drop.gte(threshold).and(event.lt(-15)).updateMask(qa)
      .unmask(0,false).rename(name).toByte();
  }
  return event.addBands(angle).addBands(valid)
    .addBands(earlyOverlap).addBands(lateOverlap)
    .addBands(preEarlyAngle.subtract(angle).abs()
      .rename(prefix+'_early_angle_diff_deg'))
    .addBands(preLateAngle.subtract(angle).abs()
      .rename(prefix+'_late_angle_diff_deg'))
    .addBands(earlyQA).addBands(lateQA)
    .addBands(earlyDrop).addBands(lateDrop)
    .addBands(mask(earlyDrop,2,earlyQA,prefix+'_early_candidate_2db'))
    .addBands(mask(earlyDrop,3,earlyQA,prefix+'_early_candidate_3db'))
    .addBands(mask(earlyDrop,4,earlyQA,prefix+'_early_candidate_4db'))
    .addBands(mask(lateDrop,3,lateQA,prefix+'_late_candidate_3db'))
    .addBands(mask(earlyDrop,3,earlyOverlap.and(lowSlope),
      prefix+'_early_candidate_3db_no_water_exclusion'));
}
var jul16=acq['2018-07-16'];
var output=preEarly.addBands(preLate)
  .addBands(preEarlyAngle).addBands(preLateAngle)
  .addBands(jul16.select('VV').rename('jul16_vv_db'))
  .addBands(jul16.select('angle').rename('jul16_angle_deg'))
  .addBands(jul16.select('VV').mask().unmask(0,false)
    .rename('jul16_valid').toByte())
  .addBands(waterValid).addBands(permanent)
  .addBands(waterKnown.toByte()).addBands(nonPermanent.toByte())
  .addBands(slope).addBands(lowSlope.toByte())
  .addBands(eventBands('2018-08-09','aug09'))
  .addBands(eventBands('2018-08-21','aug21'));
Map.centerObject(aoi,11);
Map.addLayer(preEarly,{min:-25,max:0},'June reference VV',false);
Map.addLayer(jul16.select('VV'),{min:-25,max:0},'16 July VV',false);
Map.addLayer(acq['2018-08-09'].select('VV'),{min:-25,max:0},'9 August VV',true);
Map.addLayer(acq['2018-08-21'].select('VV'),{min:-25,max:0},'21 August VV',false);
Map.addLayer(aoi,{color:'yellow'},'Pilot AOI');
if (START_EXPORTS) {
  var checks=acquisitionQA.getInfo().features.map(function(f){return f.properties;});
  if (historic.size().getInfo()!==4)
    throw new Error('Expected four pre-2018 JRC water years.');
  checks.forEach(function(c){
    if (c.scene_count!==2 ||
        c.mosaic_valid_fraction_aoi_approx_30m<0.95 ||
        c.absolute_orbits.indexOf('|')>=0)
      throw new Error('Acquisition QA failed: '+c.date_utc);
  });
  var angles=checks.map(function(c){return c.mean_incidence_angle_deg_approx;});
  if (Math.max.apply(null,angles)-Math.min.apply(null,angles)>2)
    throw new Error('Incidence-angle guard failed.');
  if (EXPORT_QA_TABLE) Export.table.toDrive({collection:acquisitionQA,
    description:'phase4_s1_2018_pilot_selected_acquisition_qa',
    fileFormat:'CSV'});
  // Earth Engine GeoTIFF exports require compatible types across all bands.
  Export.image.toDrive({image:output.toFloat(),
    description:'phase4_s1_2018_pilot_exploratory_candidate_bands',
    region:aoi,scale:30,crs:'EPSG:32643',maxPixels:1e9,fileFormat:'GeoTIFF'});
}
