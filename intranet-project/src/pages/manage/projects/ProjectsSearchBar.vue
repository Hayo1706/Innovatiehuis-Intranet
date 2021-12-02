<template>
  <div class="input-group">
    <input
      id="search-input"
      type="search"
      class="form-control"
      placeholder="Zoeken"
      v-model="searchTermField"
    />
  </div>
</template>
<script>
export default {
  name: "ProjectsSearchBar",
  props: ["searchTerm"],
  data: function () {
    return { searchTermField: null };
  },
  methods: {},
  watch: {
    searchTermField: function (val) {
      //do something when the data changes.
      if (!val) {
        this.$emit("searchBarChanged", null);
      } else {
        this.$emit("searchBarChanged", this.searchTermField);
      }
    },
    searchTerm: function (val) {
      this.searchTermField = val;
    },
  },
};
</script>
<style  scoped>
#search-input {
  margin-right: 4px;
}
</style>