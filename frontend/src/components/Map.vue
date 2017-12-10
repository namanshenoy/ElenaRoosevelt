<template lang="html">
  <div class='container'>
    <div class="sidebar">
      <div id="context">
        <div class="inputs">
        <input class ="input" id="autoInput" type="text" onfocus="this.placeholder=''" placeholder="FROM">
      </br>
        <input class ="input" id="autoInput" type="text" onfocus="this.placeholder=''" placeholder="TO">
        </div>
      <button v-on:click="calcRoute" type="submit" class="button" id="submit">Find Route</button>
      <button v-on:click="reset" type="submit" class="button" id="reset">Reset input</button>
      </div>
      <div id="datils">
      </div>
    </div>
    <div id="mapDisplay">
      <p> Loading.... </p>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      lat: 0.0,
      lng: 0.0,
      map: null
    }
  },
  mounted: function () {
    this.map = new google.maps.Map(
      document.getElementById('mapDisplay'),
      this.options
    )
    this.getCurrentLocation().then(() => { this.initMap () }).catch((err) => { alert(err) })
    this.createMarkers()
    this.initAutocomplete()
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
    },
    getCurrentLocation () {
      return new Promise((resolve, reject) => {
        if ('geolocation' in navigator) {
          var gl = navigator.geolocation
          gl.getCurrentPosition(function (position) {
            this.lng = position.coords.longitude
            this.lat = position.coords.latitude

            let latLng = new google.maps.LatLng(this.lat, this.lng)
            resolve(latLng) }.bind(this))
        } else {
          reject('Cannot use geolocation')
        }
      })
    },
    initMap () {
      this.map = new google.maps.Map(document.getElementById('mapDisplay'), {
        center: {
          lat: this.lat,
          lng: this.lng
        },
         zoom: 15
     })
      }
  }
}
</script>
<style lang="css">
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-size: 15px;
}
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}
.sidebar {
  position: absolute;
  display:flex;
  flex-flow:column;
  width: 25%;
  height: 100%;
  top: 0; left: 0;
  overflow: hidden;
  border-right: 3px solid rgba(0,0,0,0.2);
}
#mapDisplay {
  position: absolute;
  left: 25%;
  width: 75%;
  top: 0; bottom: 0
}
.input {
  margin: 8px;
  background-color: #fff;
  border: 1px solid #c4c4c4;
  height:30px;
  width:75%;
  padding:0 10px;
}
.button {
  cursor: pointer;
  outline: none;
  margin: 10px;
  border: none;
  border-top: none;
  border-left: none;
  border-right: none;
  width: 35%;
  height: 30px;
  font-family: Helvetica;
  color: white;
  border-radius: 10px;
  box-shadow: 0px 2px 7px grey;
  transition: 100ms ease;
}
#submit.button{
  border-bottom: 5px solid steelblue;
  background: linear-gradient(#5FDDFF,#53ADDF);
}
#reset.button{
  border-bottom: 5px solid #761282;
  background: linear-gradient(#ad5197,#8e3160);
}
#submit.button:active{
  color: #5FFFFF;
  transform: translateY(4px);
}
#reset.button:active{
  color: #e87cf4;
  transform: translateY(4px);
}

.button:focus {outline:0;}

</style>
