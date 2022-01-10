<template>
  <div class="container-fluid">
    <button
      id="actionButton"
      class="btn pmd-btn-fab pmd-ripple-effect btn-primary"
      data-bs-toggle="modal"
      data-bs-target="#createProjectModal"
      type="button"
    >
      <i class="material-icons pmd-sm">Project toevoegen</i>
    </button>

    <ProjectsHeader
      @searchBarChanged="setSearchTerm"
      @showUnArchivedOnly="setShowUnArchived"
      v-bind:searchTerm="this.searchTerm"
      v-bind:showUnArchivedOnly="this.showUnArchivedOnly"
    ></ProjectsHeader>
    <ProjectCreateModal></ProjectCreateModal>
    <div class="container-fluid d-sm-block d-lg-none">
      <div class="row">
        <SearchBar
          class="col"
          id="searchBarMobile"
          @searchBarChanged="setSearchTerm"
          v-bind:searchTerm="this.searchTerm"
        ></SearchBar>
        <ProjectsShowUnArchivedOnlyBox
          id="showunarchivedonlyboxMobile"
          class="col"
          @showUnArchivedOnly="setShowUnArchived"
          v-bind:showUnArchivedOnly="this.showUnArchivedOnly"
        ></ProjectsShowUnArchivedOnlyBox>
      </div>
    </div>
    <div class="container-fluid">
      <div v-for="project of filteredProjects" :key="project.project_name">
        <ProjectListing
          class="projectlisting"
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
import ProjectService from "@/services/ProjectService.js";
import ProjectListing from "./ProjectListing.vue";
import ProjectsHeader from "./ProjectsHeader.vue";
import SearchBar from "@/shared_components/SearchBar.vue";
import ProjectsShowUnArchivedOnlyBox from "./ProjectsShowUnArchivedOnlyBox.vue";
import ProjectCreateModal from "./ProjectCreateModal.vue";
export default {
  components: {
    ProjectListing,
    ProjectsHeader,
    SearchBar,
    ProjectsShowUnArchivedOnlyBox,
    ProjectCreateModal,
  },
  name: "ProjectsPage",
  data: function () {
    return {
      projects: [],
      searchTerm: null,
      showUnArchivedOnly: false,
    };
  },
  methods: {
    gotoCreateProject() {
      this.$router.push({ path: "/manage/projects/create" });
    },
    setSearchTerm(value) {
      this.searchTerm = value;
    },
    setShowUnArchived(value) {
      this.showUnArchivedOnly = value;
    },
    removeProject(id) {
      ProjectService.deleteProject(id)
        .then(() => {
          //remove the project from the view
          this.projects = this.projects.filter(function (project) {
            return project.projectid !== id;
          });
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    archiveProject(project) {
      let projectCopy = JSON.parse(JSON.stringify(project));
      projectCopy.is_archived = !projectCopy.is_archived;
      ProjectService.archiveProject(projectCopy)
        .then(() => {
          project.is_archived = !project.is_archived;
          project.last_updated = new Date();
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    shouldShow(project) {
      let shouldShow = false;
      shouldShow = this.matchesSearchTermWhenShould(project);
      if (shouldShow) {
        shouldShow = this.showArchivedWhenShould(project);
      }

      return shouldShow;
    },
    matchesSearchTermWhenShould(project) {
      if (this.searchTerm == null) {
        return true;
      } else {
        return project.project_name
          .toLowerCase()
          .includes(this.searchTerm.toLowerCase());
      }
    },
    showArchivedWhenShould(project) {
      if (!this.showUnArchivedOnly) {
        return true;
      } else {
        return project.is_archived == false;
      }
    },
  },

  computed: {
    filteredProjects() {
      return this.projects.filter((project) => {
        return this.shouldShow(project);
      });
    },
  },
  async created() {
    this.$emit("newHeaderTitle", "Projecten - Overzicht");
    ProjectService.getProjects()
      .then((response) => {
        this.projects = response;
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
      });
  },
};
</script>

<style scoped>
#searchBarMobile {
  padding-top: 5px;
  margin-top: 5px;
  margin-bottom: 5px;
  height: fit-content;
  width: 100%;
}
#noresults {
  margin-top: 10px;
  color: white;
}
#actionButton {
  position: fixed;
  bottom: 0;
  left: 0;
  margin: 20px;
  background-color: var(--gold1);
  border-color: var(--blue1);
  z-index: 10;
}
#littleSpace {
  height: 60px;
  width: 100%;
}
#showunarchivedonlyboxMobile {
  margin-top: 10px;
  color: white;
}
</style>