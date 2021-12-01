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
      <div v-for="project of projects" :key="project.name">
        <ProjectListing
          v-if="shouldShow(project)"
          @removeProject="this.removeProject"
          @archiveProject="this.archiveProject"
          v-bind:project="project"
        ></ProjectListing>
      </div>
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