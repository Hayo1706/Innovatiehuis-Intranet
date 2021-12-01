<template>
  <div class="input-group">
    <input
      id="search-input"
      type="search"
      class="form-control"
      placeholder="Zoeken"
      v-model="searchTerm"
      v-on:keyup.enter="search"
    />
    <button @click="search">Ga</button>
  </div>
</template>
<script>
export default {
  name: "ProjectsSearchBar",
  data: function () {
    return { searchTerm: "" };
  },
  methods: {
    search() {
      this.$emit("searchBarChanged", this.searchTerm);
    },
  },
  watch: {
    searchTerm: function (val) {
      //do something when the data changes.
      if (!val) {
        this.$emit("searchBarChanged", null);
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