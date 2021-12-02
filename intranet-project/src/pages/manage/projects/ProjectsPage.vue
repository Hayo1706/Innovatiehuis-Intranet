<template>
  <div>
    <ProjectsHeader @searchBarChanged="setSearchTerm"></ProjectsHeader>
    <div class="container-fluid d-sm-block d-lg-none">
      <ProjectsSearchBar
        id="searchBar"
        @searchBarChanged="setSearchTerm"
      ></ProjectsSearchBar>
    </div>
    <div class="container-fluid">
      <div v-for="project of filteredProjects" :key="project.name">
        <ProjectListing
          @removeProject="this.removeProject"
          @archiveProject="this.archiveProject"
          v-bind:project="project"
        ></ProjectListing>
      </div>
      <div v-if="filteredProjects.length == 0">Geen resultaten.</div>
    </div>
  </div>
</template>

<script>
import { deleteProject, updateProject } from "@/services/ProjectService.js";
import ProjectListing from "./ProjectListing.vue";
import ProjectsHeader from "./ProjectsHeader.vue";
import { getProjects } from "@/services/ProjectService.js";
import ProjectsSearchBar from "./ProjectsSearchBar.vue";
export default {
  components: { ProjectListing, ProjectsHeader, ProjectsSearchBar },
  name: "ProjectsPage",
  data: function () {
    return { projects: [], searchTerm: null, showArchivedOnly: false };
  },
  methods: {
    setSearchTerm(value) {
      this.searchTerm = value;
    },
    removeProject(id) {
      deleteProject(id)
        .then(() => {
          //remove the project from the view
          this.projects = this.projects.filter(function (item) {
            return item.projectid !== id;
          });
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
            alert(err);
          } else {
            alert("Network error! Connection timed out!");
          }
        });
    },
    archiveProject(project) {
      let projectCopy = JSON.parse(JSON.stringify(project));
      projectCopy.isarchived = !projectCopy.isarchived;
      updateProject(projectCopy)
        .then(() => {
          project.isarchived = !project.isarchived;
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
            alert(err);
          } else {
            alert("Network error! Connection timed out!");
          }
        });
    },
    shouldShow(item) {
      let shouldShow = false;
      shouldShow = this.matchesSearchTermWhenShould(item);
      if (shouldShow) {
        shouldShow = this.showArchivedWhenShould(item);
      }

      return shouldShow;
    },
    matchesSearchTermWhenShould(item) {
      if (this.searchTerm == null) {
        return true;
      } else {
        return item.name.toLowerCase().includes(this.searchTerm.toLowerCase());
      }
    },
    showArchivedWhenShould(item) {
      if (!this.showArchivedOnly) {
        return true;
      } else {
        return item.isarchived;
      }
    },
  },

  computed: {
    filteredProjects() {
      return this.projects.filter((item) => {
        return this.shouldShow(item);
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