<template>
  <div class="form-check form-switch">
    <input
      class="form-check-input"
      id="flexSwitchCheckChecked"
      type="checkbox"
      v-model="showArchivedField"
    />
    <label class="form-check-label" for="flexSwitchCheckChecked">Toon gearchiveerde projecten</label>
  </div>
</template>
<script>
export default {
  name: "ProjectsShowArchivedCheckbox",
  props: ["showArchived"],
  data: function () {
    return { showArchivedField: false };
  },
  methods: {},
  watch: {
    showArchivedField: function (showArchivedField) {
      this.$emit("showArchived", showArchivedField);
    },
    showArchived: function (val) {
      this.showArchivedField = val;
      console.log(this.showArchivedField);
    },
  },
};
</script>
<style  scoped>
.form-switch{
  user-select: none;
  width: fit-content;
}

</style>