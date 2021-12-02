<template>
  <div class="input-group">
    <input
      id="search-input"
      type="search"
      class="form-control"
      placeholder="Zoeken"
      v-model="searchTerm"
    />
  </div>
</template>
<script>
export default {
  name: "ProjectsSearchBar",
  data: function () {
    return { searchTerm: "" };
  },
  methods: {},
  watch: {
    searchTerm: function (val) {
      //do something when the data changes.
      if (!val) {
        this.$emit("searchBarChanged", null);
      } else {
        this.$emit("searchBarChanged", this.searchTerm);
      }
    },
  },
};
</script>
<style  scoped>
#search-input {
  margin-right: 4px;
}
</style>