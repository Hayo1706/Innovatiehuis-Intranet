<template>
  <div id="projectsHeader" class="container-fluid d-none d-lg-block">
    <div class="row">
      <div class="col">Project</div>
      <div class="col">Aangemaakt</div>
      <div class="col">Laatste Update</div>
      <div class="col">
        <SearchBar
          @searchBarChanged="
            (searchTerm) => $emit('searchBarChanged', searchTerm)
          "
          v-bind:searchTerm="this.searchTerm"
        ></SearchBar>
        <ProjectsShowUnArchivedOnlyBox
          @showUnArchivedOnly="(value) => $emit('showUnArchivedOnly', value)"
          v-bind:showUnArchivedOnly="this.showUnArchivedOnly"
        ></ProjectsShowUnArchivedOnlyBox>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from "@/shared_components/SearchBar.vue";
import ProjectsShowUnArchivedOnlyBox from "./ProjectsShowUnArchivedOnlyBox.vue";
export default {
  components: { SearchBar, ProjectsShowUnArchivedOnlyBox },
  name: "ProjectsHeader",
  props: ["searchTerm", "showUnArchivedOnly"],
  data: function () {
    return {};
  },
  methods: {},
};
</script>

<style scoped>
#projectsHeader {
  width: 100%;
  box-sizing: border-box;
  min-height: 10vh;
  background-color: var(--blue1);
  border: white 5px solid;
  margin-top: 1vh;
  color: white;
  font-size: calc(1vw + 1vh);
  padding: 20px;
  font-family: Montserrat;
  margin-bottom: 1vh;
}
.input-group {
  width: 90%;
}
#search-input {
  margin-right: 4px;
}
img {
  width: calc(2vw + 3vh);
  padding-bottom: 10px;
  padding-left: 10px;
  cursor: pointer;
}
</style>