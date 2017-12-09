<template>
  <div id="app">
    <mapcomp></mapcomp>
  </div>
</template>

<script>
import Vue from 'vue'
import MapComp from './components/MapComp'
Vue.component('mapcomp', MapComp)
export default {
  name: 'app',
  components: {
    MapComp
  }
}
</script>
<style>
* { box-sizing: border-box; }
</style>
