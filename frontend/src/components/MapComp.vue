<template>
  <div id="mapcomp">

    <div class="sidebar">
      <div id="context">
        <div id="start">
        <b>Start:&nbsp;</b>
        <input id="autoInput" type="text" placeholder="Enter a location">
        </div>
        <div id="end">
        <b>End:&nbsp;</b>
        <input id="autoInput" type="text" placeholder="Enter a location">
        </div>
        <button v-on:click="calcRoute" id="button">Find Route</button>
      </div>
      <div id="datils">
      </div>
    </div>

    <div id="mapview"></div>
  </div>
</template>
<script>
export default{
  name: 'mapcomp',
  data: {
    options: {
      zoom: 3,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      center: new google.maps.LatLng(42.391157, 72.526712)
    },
    map: '',
    locations: [
     {lat: 42.391157, lng: -72.526712}
    ],
    visibleMarkers: [],
    noVisibleMarkers: false,
    markers: [],
    currentZoom: 0,
    currentLocation: ''
  },
  methods: {
    createMarkers: function () {
      this.markers = this.locations.map(function (location, i) {
        var marker = new google.maps.Marker({
          position: location
        })
        return marker
      })
    },
    initAutocomplete: function () {
      var self = this
      var autoInput = document.getElementById('autoInput')
      var autocomplete = new google.maps.places.Autocomplete(autoInput)
      autocomplete.addListener('place_changed', function () {
        var place = autocomplete.getPlace()
        if (!place.geometry) {
          window.alert("No details available for input: '" + place.name + "'")
          return
        } else {
          if (self.currentLocation) {
            self.currentLocation.setMap(null)
          }
          self.currentLocation = new google.maps.Marker({
            position: place.geometry.location,
            id: 'currentLocation',
            map: self.map
          })
        }
        if (place.geometry.viewport) {
          self.map.fitBounds(place.geometry.viewport)
        } else {
          self.map.setCenter(place.geometry.location)
          self.map.setZoom(7)
        }
      })
    }
  },
  mounted: function () {
    this.map = new google.maps.Map(
      document.getElementById('mapview'),
      this.options
    )
    this.createMarkers()
    this.initAutocomplete()
  }
}
</script>

<style scoped>
.mapcomp {
  position: absolute;
  left: 35%;
  width: 65%;
  top: 0; bottom: 0;
}
#mapview {
  width: 100%;
  height: 500px;
  border: 1px solid black;
}
#autoInput {
  height: 50px;
  line-height: 50px;
  font-size: 30px;
  margin: 1em 0;
  padding: .25em;
}
.sidebar {
  position: absolute;
  display:flex;
  flex-flow:column;

  width: 35%;
  height: 100%;
  top: 0; left: 0;
  overflow: hidden;
  border-right: 3px solid rgba(0,0,0,0.2);
}
.inputs {
  display:flex;
  flex:1 1 0;
  min-width: 100%;
}
#context {
display:flex;
z-index:5;
padding: 10px;
background-color: #fff;
border: 2px solid #999;
}
</style>
