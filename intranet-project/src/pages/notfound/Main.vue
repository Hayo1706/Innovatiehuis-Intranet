<template>
  <div>
    Sorry! We can't seem to find the resource you're looking for. Please check
    that the Web site address is spelled correctly.
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