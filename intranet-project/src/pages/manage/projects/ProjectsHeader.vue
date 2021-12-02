<template>
  <div id="projectsHeader" class="container-fluid d-none d-lg-block">
    <div class="row">
      <div class="col">Project</div>
      <div class="col">Aangemaakt</div>
      <div class="col">Laatste Update</div>
      <div class="col">Overkoepelend project</div>
      <div class="col">Sub-projecten</div>
      <div class="col">
        <ProjectsSearchBar
          @searchBarChanged="
            (searchTerm) => $emit('searchBarChanged', searchTerm)
          "
          v-bind:searchTerm="this.searchTerm"
        ></ProjectsSearchBar>
        <ProjectsShowArchivedOnlyBox
          @showArchivedOnly="(value) => $emit('showArchivedOnly', value)"
          v-bind:showArchivedOnly="this.showArchivedOnly"
        ></ProjectsShowArchivedOnlyBox>
      </div>
    </div>
  </div>
</template>

<script>
import ProjectsSearchBar from "./ProjectsSearchBar.vue";
import ProjectsShowArchivedOnlyBox from "./ProjectsShowArchivedOnlyBox.vue";
export default {
  components: { ProjectsSearchBar, ProjectsShowArchivedOnlyBox },
  name: "ProjectsHeader",
  props: ["searchTerm", "showArchivedOnly"],
  data: function () {
    return {};
  },
  methods: {},
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
img {
  width: calc(2vw + 3vh);
  padding-bottom: 10px;
  padding-left: 10px;
  cursor: pointer;
}
</style>