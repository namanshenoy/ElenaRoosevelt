<template>
  <div class="mapcomp">
    <v-map :zoom=13 :center="[42.38681,-72.52547]">
      <v-tilelayer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"></v-tilelayer>
      <!-- <v-marker :lat-lng="[42.38681,-72.52547]"></v-marker> -->
    </v-map>
  </div>
</template>
<script>
export default {
  name: 'mapcomp'
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
