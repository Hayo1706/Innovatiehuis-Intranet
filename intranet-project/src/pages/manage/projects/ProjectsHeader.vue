<template>
  <div id="projectsHeader" class="container-fluid d-none d-lg-block">
    <div class="row">
      <div class="col">Project</div>
      <div class="col">Aangemaakt</div>
      <div class="col">Laatste Update</div>
      <div class="col">Overkoepelend project</div>
      <div class="col">Sub-projecten</div>
      <div class="col"></div>
    </div>
    <br />
  </div>
</template>

<script>
export default {
  name: "ProjectsHeader",
  data: function () {
    return {};
  },
  methods: {},
};
</script>

<style scoped>
#projectsHeader {
  font-family: AddeleSemiBold;
}
</style>