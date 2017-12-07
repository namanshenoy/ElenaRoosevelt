<template>
  <div class="mapcomp">
    <gmap-map
      :center="center"
      :zoom="14"
      style="width: 100%; height: 100%"
    >
      <gmap-marker
        :key="index"
        v-for="(m, index) in markers"
        :position="m.position"
        :clickable="true"
        :draggable="true"
        @click="center=m.position"
      ></gmap-marker>
    </gmap-map>
  </div>

</template>
<script>
  import * as VueGoogleMaps from 'vue2-google-maps'
  import Vue from 'vue'

  Vue.use(VueGoogleMaps, {
    load: {
      key: 'AIzaSyABeOw38tHkafEdgRbR2SOokc4nQApmQ-0',
      libraries: 'places'
    }
  })

  export default {
    name: 'mapcomp',
    data () {
      return {
        center: {lat: 42.391157, lng: -72.526712},
        markers: [{
          position: {lat: 42.391157, lng: -72.526712}
        }, {
          position: {lat: 42.376764, lng: -72.519573}
        }]
      }
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
</style>
