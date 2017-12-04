// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import Vue2Leaflet from 'vue2-leaflet'
import 'leaflet/dist/leaflet.css'
/* eslint-disable no-new */
Vue.component('v-map', Vue2Leaflet.Map)
Vue.component('v-tilelayer', Vue2Leaflet.TileLayer)
Vue.component('v-marker', Vue2Leaflet.Marker)
new Vue({
  el: '#app',
  template: '<App/>',
  components: { App }
})
