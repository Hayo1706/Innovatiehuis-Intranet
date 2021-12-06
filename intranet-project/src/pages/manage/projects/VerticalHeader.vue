<template>
  <div class="col">
    <div class="headerText">Project:</div>
    <div class="headerText">Aangemaakt:</div>
    <div class="headerText">Laatste Update:</div>
    <div class="headerText">
      Overkoepelend <br />
      project:
    </div>
    <br />
    <div class="headerText">Sub-projecten:</div>
  </div>
</template>

<script>
export default {
  name: "VerticalHeader",
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
.headerText {
  font-family: AddeleSemiBold;
  height: 40px;
}
</style>