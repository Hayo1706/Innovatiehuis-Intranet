<template>
  <div class="input-group">
    <input
      id="search-input"
      type="search"
      class="form-control"
      :placeholder="this.placeholder"
      v-model="searchTermField"
    />
  </div>
</template>
<script>
export default {
  name: "SearchBar",
  props: {
    placeholder: { type: String, required: true }
  },
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
        //prohibit searching for whitespace only
        if (val.trim().length == 0) {
          this.searchTermField = "";
          return;
        }

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
  background: linear-gradient(to bottom right, rgba(255,255,255,0.8), rgba(225,225,225,0.9));
}
</style>