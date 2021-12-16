<template>
  <div>
    <button
      id="actionButton"
      class="btn pmd-btn-fab pmd-ripple-effect btn-primary"
      type="button"
    >
      <i class="material-icons pmd-sm">Gebruiker toevoegen</i>
    </button>
    <ProjectsHeader
      @searchBarChanged="setSearchTerm"
      v-bind:searchTerm="this.searchTerm"
    ></ProjectsHeader>
    <div class="container-fluid d-sm-block d-lg-none">
      <div class="row">
        <ProjectsSearchBar
          class="col"
          id="searchBarMobile"
          @searchBarChanged="setSearchTerm"
          v-bind:searchTerm="this.searchTerm"
        ></ProjectsSearchBar>
        <hr />
      </div>
    </div>
    <div class="container-fluid">
      <div v-for="project of filteredProjects" :key="project.name">
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
import ProjectsSearchBar from "./ProjectsSearchBar.vue";
export default {
  components: {
    ProjectListing,
    ProjectsHeader,
    ProjectsSearchBar,
  },
  name: "ProjectsPage",
  data: function () {
    return {
      projects: [],
      searchTerm: null,
    };
  },
  methods: {
    setSearchTerm(value) {
      this.searchTerm = value;
    },
    removeProject(id) {
      ProjectService.deleteProject(id)
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
          }
          alert(err);
        });
    },
    shouldShow(item) {
      let shouldShow = false;
      shouldShow = this.matchesSearchTermWhenShould(item);
      return shouldShow;
    },
    matchesSearchTermWhenShould(item) {
      if (this.searchTerm == null) {
        return true;
      } else {
        return item.name.toLowerCase().includes(this.searchTerm.toLowerCase());
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
    this.$emit("newHeaderTitle", "Gebruikers - Overzicht");
    ProjectService.getProjects()
      .then((response) => {
        this.projects = response;
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });
  },
};
</script>

<style scoped>
#searchBarMobile {
  padding-top: 5px;
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
.projectlisting {
  padding: 10px;
}
</style>