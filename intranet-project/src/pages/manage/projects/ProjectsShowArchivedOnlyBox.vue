<template>
  <div>
    <input
      id="showarchivedonlybox"
      type="checkbox"
      name="showarchivedonlybox"
      v-model="showArchivedOnly"
    />
    <label for="showarchivedonlybox">Toon alleen gearchiveerde projecten</label>
  </div>
</template>
<script>
export default {
  name: "ProjectsShowArchivedOnlyBox",
  data: function () {
    return { showArchivedOnly: false };
  },
  methods: {},
  watch: {
    showArchivedOnly: function (val) {
      //do something when the data changes.
      if (!val) {
        this.$emit("showArchivedOnly", false);
      } else {
        this.$emit("showArchivedOnly", true);
      }
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