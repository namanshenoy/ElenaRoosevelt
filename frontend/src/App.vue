<template>
  <div id="app">
    <div class='sidebar'>
      stuff
    </div>
    <div class="map">
    <v-map :zoom=13 :center="[42.38681,-72.52547]">
      <v-tilelayer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"></v-tilelayer>
      <v-marker :lat-lng="[42.38681,-72.52547]"></v-marker>
    </v-map>
    </div>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>
<style>
* { box-sizing: border-box; }

.sidebar {
  position: absolute;
  width: 35%;
  height: 100%;
  top: 0; left: 0;
  overflow: hidden;
  border-right: 3px solid rgba(0,0,0,0.2);
}
.map {
  position: absolute;
  left: 35%;
  width: 65%;
  top: 0; bottom: 0;
}
</style>
