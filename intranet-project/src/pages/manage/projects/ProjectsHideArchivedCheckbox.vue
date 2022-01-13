<template>
  <div>
    <label for="hidarchivedcheckbox">Verberg gearchiveerde projecten</label>
    <input
      id="hidarchivedcheckbox"
      type="checkbox"
      name="hidarchivedcheckbox"
      v-model="hideArchivedField"
    />
  </div>
</template>
<script>
export default {
  name: "ProjectsHideArchivedCheckbox",
  props: ["hideArchived"],
  data: function () {
    return { hideArchivedField: false };
  },
  methods: {},
  watch: {
    hideArchivedField: function (val) {
      //do something when the data changes.
      if (!val) {
        this.$emit("hideArchived", false);
      } else {
        this.$emit("hideArchived", true);
      }
    },
    hideArchived: function (val) {
      this.hideArchivedField = val;
    },
  },
};
</script>
<style  scoped>
label {
  font-size: 15px;
  font-family: AddeleThin;
  display: inline-block;
}
input {
  display: inline-block;
}
#hidarchivedcheckbox {
  position: relative;
  top: 13px;
  margin-left: 7px;
  display: inline-block;
}
</style>