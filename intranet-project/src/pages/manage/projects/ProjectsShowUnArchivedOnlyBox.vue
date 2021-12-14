<template>
  <div>
    <input
      id="showunarchivedonlybox"
      type="checkbox"
      name="showunarchivedonlybox"
      v-model="showUnArchivedOnlyField"
    />
    <label for="showunarchivedonlybox"
      >Toon alleen ongearchiveerde projecten</label
    >
  </div>
</template>
<script>
export default {
  name: "ProjectsShowArchivedOnlyBox",
  props: ["showUnArchivedOnly"],
  data: function () {
    return { showUnArchivedOnlyField: false };
  },
  methods: {},
  watch: {
    showUnArchivedOnlyField: function (val) {
      //do something when the data changes.
      if (!val) {
        this.$emit("showUnArchivedOnly", false);
      } else {
        this.$emit("showUnArchivedOnly", true);
      }
    },
    showUnArchivedOnly: function (val) {
      this.showUnArchivedOnlyField = val;
    },
  },
};
</script>
<style  scoped>
label {
  font-size: 15px;
}
#showunarchivedonlybox {
  margin-right: 4px;
}
</style>