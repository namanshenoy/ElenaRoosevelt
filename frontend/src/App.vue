<template>
  <div id="app">
    <sidebar></sidebar>
    <mapcomp></mapcomp>
  </div>
</template>

<script>
import Vue from 'vue'
import SideBar from './components/SideBar'
import MapComp from './components/MapComp'
Vue.component('sidebar', SideBar)
Vue.component('mapcomp', MapComp)

export default {
  name: 'app',
  components: {
    MapComp, SideBar
  }
}
</script>
<style>
* { box-sizing: border-box; }
</style>
