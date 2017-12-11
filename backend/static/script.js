var points = [],
  msg_el = document.getElementById('msg'),
  url_osrm_nearest = 'http://router.project-osrm.org/nearest/v1/biking/',
  url_osrm_route = 'http://router.project-osrm.org/route/v1/biking/',
  icon_url = 'https://cdn.rawgit.com/openlayers/ol3/master/examples/data/icon.png',
  vectorSource = new ol.source.Vector(),
  vectorLayer = new ol.layer.Vector({
    source: vectorSource
  }),
  styles = {
    route: new ol.style.Style({
      stroke: new ol.style.Stroke({
        width: 6,
        color: [40, 40, 40, 0.8]
      })
    }),
    icon: new ol.style.Style({
      image: new ol.style.Icon({
        anchor: [0.5, 1],
        src: icon_url
      })
    })
  };

console.clear();

var map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    }),
    vectorLayer
  ],
  view: new ol.View({
    center: ol.proj.transform([-72.5267, 42.3912], 'EPSG:4326','EPSG:3857'),
    zoom: 15
  })
});

var data;
$("#get_route").on("click",()=>{
  console.log($SCRIPT_ROOT)

$.ajax({url: "/get_route/"+$("#origin_addr").val()+"/"+$("#destination_addr").val()+"/downhills/bike", success: function(result){
   	console.log(result.elevation_route_stats.route_node_coords)
	data = result.elevation_route_stats.route_node_coords
}});
})

//map.on('click', function(evt) {
  //console.log(evt.coordinate)
  //long = data[0]['lon']
  //lat = data[0]['lat']
  //delete data[0]

  //console.log("HEY")
  //console.log(coord)
var c = 0 //c is current node in the order of placement
function pin_drop(){

  if(c != 0){
    console.log("DIST: " + getDistanceFromLatLonInKm(data[c]['lat'],data[c]['lon'],data[c-1]['lat'],data[c-1]['lon']))
  }

  var long = data[c]['lon']
  var lat = data[c]['lat']

  cproj = ol.proj.transform([long, lat], 'EPSG:4326','EPSG:3857')

  map.getView().setCenter(cproj);
  //map.getView().setZoom(5);

  c = c+1

  utils.getNearest(cproj).then(function(coord_street) {

    var last_point = points[points.length - 1];
    var points_length = points.push(coord_street);

    utils.createFeature(coord_street);

    if (points_length < 2) {
      msg_el.innerHTML = 'Click to add another point';
      return;
    }

    //get the route
    var point1 = last_point.join();
    var point2 = coord_street.join();

    fetch(url_osrm_route + point1 + ';' + point2).then(function(r) {
      return r.json();
    }).then(function(json) {
      if (json.code !== 'Ok') {
        msg_el.innerHTML = 'No route found.';
        return;
      }
      msg_el.innerHTML = 'Route added';
      //points.length = 0;
      utils.createRoute(json.routes[0].geometry);
    });
  });
}

var features = []
var pointFeatures = []

var utils = {
  getNearest: function(coord) {
    var coord4326 = utils.to4326(coord);
    return new Promise(function(resolve, reject) {
      //make sure the coord is on street
      fetch(url_osrm_nearest + coord4326.join()).then(function(response) {
        // Convert to JSON
        return response.json();
      }).then(function(json) {
        if (json.code === 'Ok') resolve(json.waypoints[0].location);
        else reject();
      });
    });
  },
  createFeature: function(coord) {
    var feature = new ol.Feature({
      type: 'place',
      geometry: new ol.geom.Point(ol.proj.fromLonLat(coord))
    });
    feature.setStyle(styles.icon);
    pointFeatures.push(feature);
    vectorSource.addFeature(feature);
  },
  createRoute: function(polyline) {
    // route is ol.geom.LineString
    var route = new ol.format.Polyline({
      factor: 1e5
    }).readGeometry(polyline, {
      dataProjection: 'EPSG:4326',
      featureProjection: 'EPSG:3857'
    });
    var feature = new ol.Feature({
      type: 'route',
      geometry: route
    });
    feature.setStyle(styles.route);
    features.push(feature);
    vectorSource.addFeature(feature);
  },
  to4326: function(coord) {
    return ol.proj.transform([
      parseFloat(coord[0]), parseFloat(coord[1])
    ], 'EPSG:3857', 'EPSG:4326');
  }
};

function clearRoute(){
  vectorSource.clear()
  c = 0
  console.log(points)
  points = []
  features = []
  pointFeatures = []
}
function goBack(){
  vectorSource.removeFeature(features.slice(-1)[0])
  vectorSource.removeFeature(pointFeatures.slice(-1)[0])
  if (c != 0){
    c = c - 1;
    var long = data[c]['lon']
    var lat = data[c]['lat']
    cproj = ol.proj.transform([long, lat], 'EPSG:4326','EPSG:3857')
    map.getView().setCenter(cproj);
  }
  pointFeatures.pop();
  features.pop();
  points.pop();
}

function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
  var R = 6371; // Radius of the earth in km
  var dLat = deg2rad(lat2-lat1);  // deg2rad below
  var dLon = deg2rad(lon2-lon1);
  var a =
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
    Math.sin(dLon/2) * Math.sin(dLon/2)
    ;
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  var d = R * c; // Distance in km
  return d;
}

function deg2rad(deg) {
  return deg * (Math.PI/180)
}
