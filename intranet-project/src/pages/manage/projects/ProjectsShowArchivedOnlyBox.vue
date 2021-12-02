<template>
  <div>
    <input
      id="showarchivedonlybox"
      type="checkbox"
      name="showarchivedonlybox"
      v-model="showArchivedOnlyField"
    />
    <label for="showarchivedonlybox">Toon alleen gearchiveerde projecten</label>
  </div>
</template>
<script>
export default {
  name: "ProjectsShowArchivedOnlyBox",
  props: ["showArchivedOnly"],
  data: function () {
    return { showArchivedOnlyField: false };
  },
  methods: {},
  watch: {
    showArchivedOnlyField: function (val) {
      //do something when the data changes.
      if (!val) {
        this.$emit("showArchivedOnly", false);
      } else {
        this.$emit("showArchivedOnly", true);
      }
    },
    showArchivedOnly: function (val) {
      this.showArchivedOnlyField = val;
    },
  },
};
</script>
<style  scoped>
label {
  font-size: 15px;
}
#showarchivedonlybox {
  margin-right: 4px;
}
</style>