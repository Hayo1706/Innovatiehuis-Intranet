<template>
  <div>
    <ProjectsHeader @searchBarChanged="setSearchTerm"></ProjectsHeader>
    <div class="container-fluid d-sm-block d-lg-none">
      <ProjectsSearchBar
        id="searchBar"
        @searchBarChanged="setSearchTerm"
      ></ProjectsSearchBar>
    </div>

    <div v-for="project of projects" :key="project.name">
      <ProjectListing
        v-if="shouldShow(project)"
        @removeProject="this.removeProject"
        v-bind:project="project"
      ></ProjectListing>
    </div>
  </div>
</template>

<script>
import ProjectListing from "./ProjectListing.vue";
import ProjectsHeader from "./ProjectsHeader.vue";
import { getProjects } from "@/services/ProjectService.js";
import ProjectsSearchBar from "./ProjectsSearchBar.vue";
export default {
  components: { ProjectListing, ProjectsHeader, ProjectsSearchBar },
  name: "ProjectsPage",
  data: function () {
    return { projects: [], searchTerm: "" };
  },
  methods: {
    setSearchTerm(value) {
      this.searchTerm = value;
    },
    shouldShow(project) {
      if (this.searchTerm == null) {
        return true;
      } else {
        return project.name
          .toLowerCase()
          .includes(this.searchTerm.toLowerCase());
      }
    },
    removeProject(id) {
      this.projects = this.projects.filter(function (item) {
        return item.projectid !== id;
      });
    },
  },
  async created() {
    this.$emit("loaded", "Projecten - Overzicht");
    getProjects()
      .then((response) => {
        this.projects = response;
      })
      .catch((err) => {
        console.log(err);
        if (!err.response) {
          alert("Network error! Connection timed out!");
        }
      });
  },
};
</script>

<style scoped>
#searchBar {
  margin-top: 5px;
  width: 50%;
}
</style>