<template>
  <div class="col">
    <div class="headerText extraLarge">Gebruiker</div>
    <div class="headerText">Email</div>
    <div class="headerText">Telefoonnummer</div>
    <div class="headerText">Geregistreerd</div>
    <div class="headerText">Laatst gezien</div>
    <div class="headerText">Rol</div>
    <div class="headerText">projecten</div>
    <div class="headerText">Toegang</div>
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
.col {
  padding-top: 12px;
}
.headerText {
  font-family: Montserrat;
  height: 50px;
  font-size: calc(1vw + 1vh);
}
.extraLarge {
  height: 70px;
}
</style>