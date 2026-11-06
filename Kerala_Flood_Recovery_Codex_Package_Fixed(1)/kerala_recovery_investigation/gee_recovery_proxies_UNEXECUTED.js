/*
Kerala post-flood recovery proxy exports (Google Earth Engine Code Editor).
STATUS: Draft code, NOT executed or validated in an authenticated GEE project.
Purpose: independently generate district vegetation, night lights and rainfall
series; does NOT claim these directly measure household/economic recovery.

Check ADMIN district names and boundaries before use; reconcile with agricultural
statistics district codes. Prefer local controls in later analyses.
*/
var districts = ee.FeatureCollection('FAO/GAUL/2015/level2')
  .filter(ee.Filter.eq('ADM0_NAME', 'India'))
  .filter(ee.Filter.eq('ADM1_NAME', 'Kerala'));
print('Kerala districts; verify 14 and spellings', districts.size(), districts.aggregate_array('ADM2_NAME'));
Map.centerObject(districts, 8);
Map.addLayer(districts, {}, 'GAUL district boundaries');

// Landsat 8 Collection 2 surface reflectance (effective scale 30 m).
function landsatNDVI(im) {
  var qa = im.select('QA_PIXEL');
  // Mask: fill, dilated cloud, cirrus, cloud, shadow, and snow (bits 0-5).
  var clear = qa.bitwiseAnd(63).eq(0);
  var optical = im.select(['SR_B4','SR_B5','SR_B6'], ['red','nir','swir'])
    .multiply(0.0000275).add(-0.2);
  var ndvi = optical.normalizedDifference(['nir','red']).rename('ndvi');
  var ndmi = optical.normalizedDifference(['nir','swir']).rename('ndmi');
  return ndvi.addBands(ndmi).updateMask(clear).copyProperties(im,['system:time_start']);
}
var landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
  .filterBounds(districts).map(landsatNDVI);

// Equal calendar quarters preserve seasonality; low valid observation quarters
// should be excluded rather than treated as zero vegetation.
var quarters = ee.List.sequence(2016,2021).map(function(y) {
  return ee.List.sequence(0,3).map(function(q) {
    var start=ee.Date.fromYMD(ee.Number(y),1,1).advance(ee.Number(q).multiply(3),'month');
    var end=start.advance(3,'month');
    var ic=landsat.filterDate(start,end);
    var comp=ic.median();
    var valid=ic.select('ndvi').count().rename('valid_obs');
    var layers=comp.select(['ndvi','ndmi']).addBands(valid);
    return layers.reduceRegions({collection:districts,reducer:ee.Reducer.mean(),scale:60})
      .map(function(f) {return f.set({'year':y,'quarter':ee.Number(q).add(1),'start':start.format('YYYY-MM-dd'),
                                    'source':'Landsat 8 L2','n_scenes':ic.size()});});
  });
}).flatten();
Export.table.toDrive({collection:ee.FeatureCollection(quarters).flatten(),
  description:'kerala_district_landsat_ndvi_ndmi_2016_2021',
  fileFormat:'CSV', selectors:['ADM2_NAME','year','quarter','start','ndvi','ndmi','valid_obs','n_scenes','source']});

// VIIRS monthly DNB average radiance (nighttime illumination *proxy*, not income).
// cf_cvg is the number of cloud-free observations; threshold can be sensitivity-tested.
var viirs = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG')
  .filterBounds(districts);
var night = ee.List.sequence(2016,2021).map(function(y) {
  return ee.List.sequence(1,12).map(function(mm) {
    var start=ee.Date.fromYMD(ee.Number(y),ee.Number(mm),1);
    var ic=viirs.filterDate(start,start.advance(1,'month'));
    var im=ee.Image(ic.first());
    var bright=im.select('avg_rad').updateMask(im.select('cf_cvg').gte(3)).rename('night_radiance');
    var cov=im.select('cf_cvg').rename('cloudfree_obs');
    return bright.addBands(cov).reduceRegions({collection:districts,reducer:ee.Reducer.mean(),scale:750})
      .map(function(f) {return f.set({'year':y,'month':mm,'source':'VIIRS VCMSLCFG'});});
  });
}).flatten();
Export.table.toDrive({collection:ee.FeatureCollection(night).flatten(),
  description:'kerala_district_viirs_monthly_2016_2021',
  fileFormat:'CSV', selectors:['ADM2_NAME','year','month','night_radiance','cloudfree_obs','source']});

// Seasonal rainfall to adjust for differing monsoon conditions; not an observed
// recovery outcome. CHIRPS resolution is ~5 km; no false 30 m spatial detail.
var chirps=ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY').filterBounds(districts);
var rain=ee.List.sequence(2016,2021).map(function(y) {
 var start=ee.Date.fromYMD(ee.Number(y),6,1);
 var end=ee.Date.fromYMD(ee.Number(y),10,1);
 var img=chirps.filterDate(start,end).select('precipitation').sum().rename('monsoon_rain_mm');
 return img.reduceRegions({collection:districts,reducer:ee.Reducer.mean(),scale:6000})
    .map(function(f){return f.set({'year':y,'source':'CHIRPS daily'});});
});
Export.table.toDrive({collection:ee.FeatureCollection(rain).flatten(),
  description:'kerala_district_chirps_monsoon_rain_2016_2021',
  fileFormat:'CSV', selectors:['ADM2_NAME','year','monsoon_rain_mm','source']});

// Required before any manuscript use: review zero-image periods, available
// coverage, orbit/scene gaps, cloud contamination, district boundary comparability,
// season-corrected baselines, trend controls, and flood-exposure alignment.
