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
    placeholder: { type: String, required: true },
    searchTerm: { type: String, required: true },
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
  font-size: 16px;
  height: 34px;
  background-color: #f5f5f5;
  background-image: url("../assets/images/search_icon.png");
  background-size: 24px;
  background-position: 5px 5px; 
  background-repeat: no-repeat;
  padding: 12px 20px 12px 40px;
  outline: none;
  margin-right: 4px;
  border-style: solid;
}
</style>