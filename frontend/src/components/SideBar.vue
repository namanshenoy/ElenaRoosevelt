<template>
  <div class="sidebar">
    <div id="context">
    	<b>Start:&nbsp;</b>
    	<input type="text" id="start" value="boston" placeholder="Start"/>
      <br>
    	<b>End:&nbsp;</b>
    	<input type="text" id="end" value="Malden" placeholder="End"/>
      <br>
    	<input type="button" id="submit" value="Find Route" />
    </div>
  </div>
</template>
<script>

export default {
  name: 'sidebar',
  components: {
    // Detail
    // Trip
  }
}
</script>
<style scoped>
.sidebar {
  position: absolute;
  width: 35%;
  height: 100%;
  top: 0; left: 0;
  overflow: hidden;
  border-right: 3px solid rgba(0,0,0,0.2);
}
#context {
position: absolute;
z-index:5;
padding: 10px;
background-color: #fff;
border: 2px solid #999;
}
</style>
