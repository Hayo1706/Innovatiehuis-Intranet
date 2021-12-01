<template>
  <div id="projectsHeader" class="container-fluid d-none d-lg-block">
    <div class="row">
      <div class="col">Project</div>
      <div class="col">Aangemaakt</div>
      <div class="col">Laatste Update</div>
      <div class="col">Overkoepelend project</div>
      <div class="col">Sub-projecten</div>
      <div class="col">
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
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProjectsHeader",
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

<style scoped>
#projectsHeader {
  font-family: AddeleSemiBold;
  width: 100%;
  box-sizing: border-box;
  min-height: 10vh;
  background-color: var(--blue1);
  border-top: white 2px solid;
  color: white;
  font-size: calc(1vw + 1vh);
  padding: 20px;
  font-family: AddeleSemiBold;
}
.input-group {
  width: 90%;
}
#search-input {
  margin-right: 4px;
}
</style>