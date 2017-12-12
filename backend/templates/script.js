var points = [],
  msg_el = document.getElementById('msg'),
  url_osrm_nearest = 'http://router.project-osrm.org/nearest/v1/bike/',
  url_osrm_route = 'http://router.project-osrm.org/route/v1/bike/',
  icon_url = 'https://vasco.eu/sites/all/themes/vasco/includes/img/marker.png',
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
  document.getElementById("msg").innerHTML = "Loading route.."
$.ajax({url: "http://35.227.65.115:7000/get_route/"+$("#origin_addr").val()+"/"+$("#destination_addr").val()+"/"+$('input[name=radio]:checked').val()+"/bike", success: function(result){
  //console.log(result.elevation_route_stats.route_node_coords)
  data = result.elevation_route_stats.route_node_coords
  document.getElementById("msg").innerHTML = "Route found! Click next pin"
  document.getElementById("chart_div").innerHTML = ""

  stats = result.elevation_route_stats.route_grades_stats

  document.getElementById("go_back").disabled=true
  data_chart = result.elevation_route_stats.route_elevations_with_distances
  while(!data_chart){
    console.log("DATA CHART")
    console.log(data_chart)
    $.ajax({url: "http://35.227.65.115:7000/get_route/"+$("#origin_addr").val()+"/"+$("#destination_addr").val()+"/"+$('input[name=radio]:checked').val()+"/bike", success: function(result){
        console.log(result.elevation_route_stats.route_node_coords)
        data_chart = result.elevation_route_stats.route_elevations_with_distances}
      })
    }
  console.log("DATA CHART")
  console.log(data_chart)
  totalDistance = Math.round(data_chart[data_chart.length - 1].distance);
     console.log("DATA")
      let elevGain = data.reduce((acc, cur, idx, arr) => {
        if (idx > 0 && (cur.elevation > arr[idx - 1].elevation)) {
          acc += cur.elevation - arr[idx - 1].elevation;
        }
        return acc;
      }, 0);
      elevGain = Math.round(elevGain * 3.28084);
      const chartMargins = {
        top: 10,
        right: 10,
        bottom: 50,
        left: 50
      };
      const chartWidth = parseInt(d3.select('#chart_div').style('width'), 10);
      const chartHeight = 300;
      const width = chartWidth - chartMargins.right - chartMargins.left;
      const height = chartHeight - chartMargins.top - chartMargins.bottom;
      const svg = d3.select('#chart_div').append('svg')
        .attr('width', chartWidth)
        .attr('height', chartHeight);
      const g = svg.append('g')
        .attr('transform', "translate(" + chartMargins.left + "," + chartMargins.top + ")");
      const xScale = d3.scaleLinear()
        .range([0, width])
        .domain(d3.extent(data_chart, d => d.distance));
      const yScale = d3.scaleLinear()
        .range([height, 0])
        .domain(d3.extent(data_chart, d => d.elevation));
      const areaFn = d3.area()
        .x(d => xScale(d.distance))
        .y0(yScale(d3.min(data_chart, d => d.elevation)))
        .y1(d => yScale(d.elevation))
        .curve(d3.curveBasis);
      g.append('path')
        .datum(data_chart)
        .attr('fill', 'steelblue')
        .attr('d', areaFn);
      /*g.append('g')
          .attr('transform', `translate(0, ${height})`)
          .call(d3.axisBottom(xScale))
        .append('text')
          .attr('fill', '#333')
          .attr('y', 35)
          .attr('x', width / 2)
          .text('Distance in meters');*/
      g.append('g')
          .call(d3.axisLeft(yScale))
        .append('text')
          .attr('fill', '#333')
          .attr('transform', 'rotate(-90)')
          .attr('y', -35)
          .attr('x', -height / 2)
          .attr('text-anchor', 'end')
          .text('Height, in meters');

      // label for total distance
    /*  g.append('g')
        .append('text')
          .classed('heading', true)
          .attr('y', height + 35)
          .attr('x', 0)
          .attr('font-family', 'sans-serif')
          .text('Total distance:')
        .append('tspan')
          .text(` ${totalDistance} m`);*/
      // label for total elevation gain
      /*g.append('g')
        .append('text')
          .classed('heading', true)
          .attr('y', height + 35)
          .attr('x', width)
          .attr('font-family', 'sans-serif')
          .attr('text-anchor', 'end')
          .attr('startOffset', '100%')
          .text('Elevation gain:')
        .append('tspan')
          .text(` ${elevGain.toLocaleString()} ft`);*/
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

  if(points.length >= data.length){
    console.log("YES")
    msg_el.innerHTML = 'Route complete'
    document.getElementById("next_pin").disabled = true
  }

  if(c != 0){
    console.log("DIST: " + getDistanceFromLatLonInKm(data[c]['lat'],data[c]['lon'],data[c-1]['lat'],data[c-1]['lon']))
  }

  var long = data[c]['lon']
  var lat = data[c]['lat']

  cproj = ol.proj.transform([long, lat], 'EPSG:4326','EPSG:3857')

  map.getView().setCenter(cproj);
  //map.getView().setZoom(5);


  utils.getNearest(cproj).then(function(coord_street) {

    var last_point = points[points.length - 1];
    var points_length = points.push(coord_street);

    utils.createFeature(coord_street);

    if(points_length > 1 && document.getElementById("go_back").disabled == true){
      document.getElementById("go_back").disabled=false;
    }

    if (points_length > 1) {
      hill = "flat "
      if(stats.grades_list[c-2] > 0){
        hill = "uphill "
      }else{
        hill = "downhill "
      }
      deg_bearing = bearings(data[c-1]['lat'],data[c-1]['lon'],data[c]['lat'],data[c]['lon'])
      console.log(deg_bearing)
      bearing = ''
      if (deg_bearing > 0 && deg_bearing < 22.5){
        bearing = 'North'
      }
      else if (deg_bearing > 337.5 && deg_bearing < 360){
        bearing = 'North'
      }
      else if (deg_bearing > 22.5 && deg_bearing < 67.5){
        bearing = 'North-East'
      }
      else if (deg_bearing > 67.5 && deg_bearing < 112.5){
        bearing = 'East'
      }
      else if (deg_bearing > 112.5 && deg_bearing < 157.5){
        bearing = 'South-East'
      }
      else if (deg_bearing > 157.5 && deg_bearing < 202.5){
        bearing = 'South'
      }
      else if (deg_bearing > 202.5 && deg_bearing < 247.5){
        bearing = 'South-West'
      }
      else if (deg_bearing > 247.5 && deg_bearing < 292.5){
        bearing = 'West'
      }
      else if (deg_bearing > 292.5 && deg_bearing < 337.5){
        bearing = 'North'
      }

      msg_el.innerHTML = 'Continue ' + hill + Math.round(getDistanceFromLatLonInKm(data[c-1]['lat'],data[c-1]['lon'],data[c-2]['lat'],data[c-2]['lon'])) + 'ft ' +bearing;
    }




    //get the route
    var point1 = last_point.join();
    var point2 = coord_street.join();

    fetch(url_osrm_route + point1 + ';' + point2).then(function(r) {
      return r.json();
    }).then(function(json) {
      if (json.code !== 'Ok') {
        return;
      }
      //points.length = 0;
      //utils.createRoute(json.routes[0].geometry);

    });
  });
  c = c + 1;
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
  if(document.getElementById("next_pin").disabled == true){
    document.getElementById("next_pin").disabled = false
  }
}
function goBack(){
  if(features.length != 0){
  vectorSource.removeFeature(features.slice(-1)[0])
  }
  if(pointFeatures.length != 0){
    vectorSource.removeFeature(pointFeatures.slice(-1)[0])
  }
  if(document.getElementById("next_pin").disabled == true){
    document.getElementById("next_pin").disabled = false
  }
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
  if(points.length == 1){
    document.getElementById("go_back").disabled=true;
  }
}

function forceLoad(){
  document.getElementById("page-load").style.display="none";
}

function bearings(lat1,lng1,lat2,lng2) {
        var dLon = (lng2-lng1);
        var y = Math.sin(dLon) * Math.cos(lat2);
        var x = Math.cos(lat1)*Math.sin(lat2) - Math.sin(lat1)*Math.cos(lat2)*Math.cos(dLon);
        var brng = rad2deg(Math.atan2(y, x));
        return 360 - ((brng + 360) % 360);
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
  return d*3280.84; //now it's in feet
}

function deg2rad(deg) {
  return deg * (Math.PI/180)
}

function rad2deg(rad) {
  return rad * 180 / Math.PI;
}

$(document).ready(function(){
       //Here is my logic now
       var input_origin = document.getElementById('origin_addr');
       var input_destination = document.getElementById('destination_addr');

       var autocomplete_origin = new google.maps.places.Autocomplete(input_origin);
       var autocomplete_destination = new google.maps.places.Autocomplete(input_destination);

       autocomplete_origin.addListener('place_changed', function() {
           infowindow.close();
           marker.setVisible(false);
           var place = autocomplete_origin.getPlace();
           console.log(place)
           if (!place.geometry) {
             // User entered the name of a Place that was not suggested and
             // pressed the Enter key, or the Place Details request failed.
             window.alert("No details available for input: '" + place.name + "'");
             return;
           }
       })

       autocomplete_destination.addListener('place_changed', function() {
           infowindow.close();
           marker.setVisible(false);
           var place = autocomplete_destination.getPlace();
           console.log(place)
           if (!place.geometry) {
             // User entered the name of a Place that was not suggested and
             // pressed the Enter key, or the Place Details request failed.
             window.alert("No details available for input: '" + place.name + "'");
             return;
           }
       })


   });
