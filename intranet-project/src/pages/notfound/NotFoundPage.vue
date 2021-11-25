<template>
  <div>Sorry! De pagina waar je naar zoekt kan niet gevonden worden!
    <br>
    <router-link to="/home" id="golden-button">Terug naar Hoofdpagina</router-link>
  </div>

  
</template>

<script>
export default {
  components: {},
  name: "NotFoundPage",
  data: function () {
    return {};
  },
  created() {
    this.$emit("loaded", "404 - Page not found");
  },
};
</script>

<style scoped>
#golden-button {
  color: aliceblue;
  background-color: chocolate;
  border-style: outset;
  border-radius: 8px;
  border-spacing: 20px;
  text-decoration: none;
}
</style>