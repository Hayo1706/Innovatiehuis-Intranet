<template>
  <div class="col">
    <div class="headerText">Gebruiker:</div>
    <div class="headerText">Geregistreerd:</div>
    <div class="headerText">Laatst gezien:</div>
    <div class="headerText">Rol:</div>
    <div class="headerText">projecten:</div>
    <div class="headerText">screening:</div>
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
  height: 53px;
}
</style>