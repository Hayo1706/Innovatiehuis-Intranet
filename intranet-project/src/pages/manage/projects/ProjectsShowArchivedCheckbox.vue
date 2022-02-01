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
  font-size: 1.3em;
  padding-right: 30px;
  padding-bottom: 4px;
}
.form-check-input {
  margin-bottom: 4px;
  margin-right: 8px;
}
/* .form-check-label {

} */
.form-switch .form-check-input:checked{
  background-color: var(--blue2);
}
/* .form-check-input:focus{
  background-color: darkgreen;
} */

</style>