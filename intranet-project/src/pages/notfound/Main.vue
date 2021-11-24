<template>
  <div>Sorry! De pagina waar je naar zoekt kan niet gevonden worden!</div>
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