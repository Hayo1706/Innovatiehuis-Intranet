<template>
  <div class="component-container" style="margin-left:10vw;">
    <div class="component-header">
      Sorry! De pagina waar je naar zoekt kan niet gevonden worden!
    </div>
    <div class="component-body">
      <router-link to="/home" class="full-button" style="width:fit-content">Terug naar Hoofdpagina</router-link>
    </div>
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
    this.$emit("newHeaderTitle", "404 - Page not found");
  },
};
</script>