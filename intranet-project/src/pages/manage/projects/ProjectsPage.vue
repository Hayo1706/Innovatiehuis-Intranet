<template>
  <div>
    <button
      @click="gotoCreateProject()"
      id="actionButton"
      class="btn pmd-btn-fab pmd-ripple-effect btn-primary"
      type="button"
    >
      <i class="material-icons pmd-sm">Project toevoegen</i>
    </button>
    <ProjectsHeader
      @searchBarChanged="setSearchTerm"
      @showArchivedOnly="setShowArchived"
      v-bind:searchTerm="this.searchTerm"
      v-bind:showArchivedOnly="this.showArchivedOnly"
    ></ProjectsHeader>
    <div class="container-fluid d-sm-block d-lg-none">
      <div class="row">
        <ProjectsSearchBar
          class="col"
          id="searchBarMobile"
          @searchBarChanged="setSearchTerm"
          v-bind:searchTerm="this.searchTerm"
        ></ProjectsSearchBar>
        <ProjectsShowArchivedOnlyBox
          id="showarchivedonlyboxMobile"
          class="col"
          @showArchivedOnly="setShowArchived"
          v-bind:showArchivedOnly="this.showArchivedOnly"
        ></ProjectsShowArchivedOnlyBox>
        <hr />
      </div>
    </div>
    <div class="container-fluid">
      <div v-for="project of filteredProjects" :key="project.name">
        <ProjectListing
          @removeProject="this.removeProject"
          @archiveProject="this.archiveProject"
          v-bind:project="project"
        ></ProjectListing>
      </div>
      <div id="noresults" v-if="filteredProjects.length == 0">
        Geen resultaten.
      </div>
    </div>
    <div id="littleSpace"></div>
  </div>
</template>

<script>
import { deleteProject, updateProject } from "@/services/ProjectService.js";
import ProjectListing from "./ProjectListing.vue";
import ProjectsHeader from "./ProjectsHeader.vue";
import { getProjects } from "@/services/ProjectService.js";
import ProjectsSearchBar from "./ProjectsSearchBar.vue";
import ProjectsShowArchivedOnlyBox from "./ProjectsShowArchivedOnlyBox.vue";
export default {
  components: {
    ProjectListing,
    ProjectsHeader,
    ProjectsSearchBar,
    ProjectsShowArchivedOnlyBox,
  },
  name: "ProjectsPage",
  data: function () {
    return { projects: [], searchTerm: null, showArchivedOnly: false };
  },
  methods: {
    gotoCreateProject() {
      this.$router.push({ path: "/manage/projects/create" });
    },
    setSearchTerm(value) {
      this.searchTerm = value;
    },
    setShowArchived(value) {
      this.showArchivedOnly = value;
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
#searchBarMobile {
  margin-top: 5px;
  margin-bottom: 5px;
  width: 100%;
}
#noresults {
  margin-top: 10px;
}
#actionButton {
  position: fixed;
  bottom: 0;
  left: 0;
  margin: 20px;
  background-color: var(--gold1);
  border-color: var(--blue1);
}
#littleSpace {
  height: 60px;
  width: 100%;
}
#showarchivedonlyboxMobile {
  margin-top: 10px;
}
</style>