<template>
  <div class="component-container" style="margin-left: 10vw">
    <div class="component-header">
      Je hebt geen toegang tot het platform. Neem contact op met een admin.
    </div>
    <div class="component-body"></div>
  </div>
</template>

<script>
export default {
  components: {},
  name: "NoAccessPage",
  data: function () {
    return {};
  },
  created() {
    this.$emit("newHeaderTitle", "Toegang geweigerd");
  },
};
</script>