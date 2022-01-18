<template>
  <div class="container-fluid">
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css"
    />
    <button
      id="actionButton"
      class="btn pmd-btn-fab pmd-ripple-effect btn-primary"
      data-bs-toggle="modal"
      data-bs-target="#createProjectModal"
      type="button"
      v-show="canCreate()"
    >
      <i class="material-icons pmd-sm">Project toevoegen</i>
    </button>

    <ProjectsHeader
      class="component-header"
      v-bind:sortingMethod="this.sortingMethod"
      v-bind:ascending="this.ascending"
      @sortEvent="
        (sortingTerm) => {
          sort(sortingTerm);
        }
      "
      @searchBarChanged="setSearchTerm"
      @hideArchived="setHideArchived"
      v-bind:searchTerm="this.searchTerm"
      v-bind:hideArchived="this.hideArchived"
    ></ProjectsHeader>

    <div class="container-fluid d-sm-block d-lg-none" id="sorting_space">
      <p>Sorteren op:</p>
      <div class="row">
        <button class="full-button col-3" @click="sort('name')">
          Naam
          <span v-if="sortingMethod == 'name'"
            ><i v-if="this.ascending" class="bi-caret-down-fill"></i
            ><i v-else class="bi-caret-up-fill"></i
          ></span></button
        ><button class="full-button col-3" @click="sort('created')">
          Aanmaakdatum
          <span v-if="sortingMethod == 'created'"
            ><i v-if="this.ascending" class="bi-caret-down-fill"></i
            ><i v-else class="bi-caret-up-fill"></i
          ></span>
        </button>
        <button class="full-button col-3" @click="sort('last_updated')">
          Laatste update
          <span v-if="sortingMethod == 'last_updated'"
            ><i v-if="this.ascending" class="bi-caret-down-fill"></i
            ><i v-else class="bi-caret-up-fill"></i
          ></span>
        </button>
        <button class="full-button col-3" @click="sort('archive_status')">
          Archiveerstatus
          <span v-if="sortingMethod == 'archive_status'"
            ><i v-if="this.ascending" class="bi-caret-down-fill"></i
            ><i v-else class="bi-caret-up-fill"></i
          ></span>
        </button>
      </div>
    </div>
    <ProjectCreateModal @reloadProjects="loadProjects()"></ProjectCreateModal>
    <div class="container-fluid d-sm-block d-lg-none">
      <div class="row">
        <SearchBar
          class="col"
          id="searchBarMobile"
          @searchBarChanged="setSearchTerm"
          v-bind:searchTerm="this.searchTerm"
        ></SearchBar>
        <Projectshidarchivedcheckbox
          id="hidarchivedcheckboxMobile"
          class="col"
          @hideArchived="setHideArchived"
          v-bind:hideArchived="this.hideArchived"
        ></Projectshidarchivedcheckbox>
      </div>
    </div>
    <div class="listing-container container-fluid">
      <ProjectListing v-for="project of filteredProjects" :key="project.project_name"
        class="projectlisting"
        @removeProject="this.removeProject"
        @archiveProject="this.archiveProject"
        v-bind:project="project"
      ></ProjectListing>
      <div id="noresults" v-if="filteredProjects.length == 0">
        Geen resultaten.
      </div>
    </div>
    <div id="littleSpace"></div>
  </div>
</template>

<script>
import PermissionService from "@/services/PermissionService.js";
import ProjectService from "@/services/ProjectService.js";
import ProjectListing from "./ProjectListing.vue";
import ProjectsHeader from "./ProjectsHeader.vue";
import SearchBar from "@/shared_components/SearchBar.vue";
import Projectshidarchivedcheckbox from "./ProjectsHideArchivedCheckbox.vue";
import ProjectCreateModal from "./ProjectCreateModal.vue";
export default {
  components: {
    ProjectListing,
    ProjectsHeader,
    SearchBar,
    Projectshidarchivedcheckbox,
    ProjectCreateModal,
  },
  name: "ProjectsPage",
  data: function () {
    return {
      projects: [],
      searchTerm: null,
      hideArchived: true,
      sortingMethod: "name",
      ascending: true,
    };
  },
  methods: {
    canCreate() {
      return PermissionService.userHasPermission("may_create_project");
    },
    gotoCreateProject() {
      this.$router.push({ path: "/manage/projects/create" });
    },
    setSearchTerm(value) {
      this.searchTerm = value;
    },
    setHideArchived(value) {
      this.hideArchived = value;
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
      if (!this.hideArchived) {
        return true;
      } else {
        return project.is_archived == false;
      }
    },
    sort(method) {
      if (this.sortingMethod != method) {
        this.sortingMethod = method;
        this.ascending = true;
      } else {
        this.ascending = !this.ascending;
      }
    },
    sortingFunction(a, b) {
      if (this.ascending) {
        if (a < b) {
          return -1;
        }
        if (a > b) {
          return 1;
        }
      } else {
        if (a > b) {
          return -1;
        }
        if (a < b) {
          return 1;
        }
      }
      return 0;
    },
    loadProjects(){
            ProjectService.getProjects()
      .then((response) => {
        this.projects = response;
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
      });
    }
  },

  computed: {
    filteredProjects() {
      let filteredProjects = this.projects.filter((project) => {
        return this.shouldShow(project);
      });

      if (this.sortingMethod == "name") {
        filteredProjects = filteredProjects.sort((a, b) => {
          let fa = a.project_name.toLowerCase(),
            fb = b.project_name.toLowerCase();
          return this.sortingFunction(fa, fb);
        });
      } else if (this.sortingMethod == "created") {
        filteredProjects = filteredProjects.sort((a, b) => {
          let fa = a.created,
            fb = b.created;
          return this.sortingFunction(fa, fb);
        });
      } else if (this.sortingMethod == "last_updated") {
        filteredProjects = filteredProjects.sort((a, b) => {
          let fa = a.last_updated,
            fb = b.last_updated;
          return this.sortingFunction(fa, fb);
        });
      } else if (this.sortingMethod == "archive_status") {
        filteredProjects = filteredProjects.sort((a, b) => {
          let fa = a.is_archived,
            fb = b.is_archived;
          return this.sortingFunction(fa, fb);
        });
      }
      return filteredProjects;
    },
  },
  async created() {
    this.$emit("newHeaderTitle", "Projecten - Overzicht");
    this.loadProjects();
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
.listing-container {
  padding: 0;
  border-radius: 0px 0px 10px 10px;
  background-color: rgba(255,255,255,0.3)
}
.container{
  padding: 0;
}
#noresults {
  margin-top: 10px;
  color: white;
}
#actionButton {
  position: fixed;
  bottom: 0;
  right: 0;
  margin: 20px;
  background-color: var(--gold1);
  border-color: var(--blue1);
  z-index: 10;
}
#littleSpace {
  height: 60px;
  width: 100%;
}
#hidarchivedcheckboxMobile {
  margin-top: 10px;
  color: white;
}
p {
  font-family: AddeleSemiBold;
  font-size: 20px;
}
.bi-caret-down-fill {
  margin-left: 5px;
}
.bi-caret-up-fill {
  margin-left: 5px;
}
#sorting_space {
  padding: 20px;
  box-sizing: border-box;
  color: var(--blue1);
  overflow: visible;
  background: linear-gradient(
    to right top,
    rgba(230, 230, 230, 0.7),
    rgba(230, 230, 230, 0.9)
  );
  border-radius: 1rem;
  margin-bottom: 1vh;
  font-size: 1.7vh;
  border: solid var(--gold1) 2px;
}
.full-button {
  width: fit-content;
}
</style>