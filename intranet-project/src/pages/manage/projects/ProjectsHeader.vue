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
  width: 100%;
  box-sizing: border-box;
  min-height: 10vh;
  background-color: var(--blue1);
  border-top: white 2px solid;
  color: white;
  font-size: calc(1vw + 1vh);
  padding: 20px;
  font-family: AddeleSemiBold;
}
</style>