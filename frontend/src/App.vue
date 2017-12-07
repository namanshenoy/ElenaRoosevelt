<template>
  <div id="app">
    <sidebar></sidebar>
    <mapcomp></mapcomp>

  </div>
</template>

<script>
import Vue from 'vue'
import MapComp from './components/MapComp'
import SideBar from './components/SideBar'
Vue.component('mapcomp', MapComp)
Vue.component('sidebar', SideBar)

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
