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
      @showUnArchivedOnly="setShowUnArchived"
      v-bind:searchTerm="this.searchTerm"
      v-bind:showUnArchivedOnly="this.showUnArchivedOnly"
    ></ProjectsHeader>
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
import SearchBar from "@/shared_components/SearchBar.vue";
import ProjectsShowUnArchivedOnlyBox from "./ProjectsShowUnArchivedOnlyBox.vue";
export default {
  components: {
    ProjectListing,
    ProjectsHeader,
    SearchBar,
    ProjectsShowUnArchivedOnlyBox,
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
    archiveProject(project) {
      let projectCopy = JSON.parse(JSON.stringify(project));
      projectCopy.isarchived = !projectCopy.isarchived;
      ProjectService.updateProject(projectCopy)
        .then(() => {
          project.isarchived = !project.isarchived;
          project.lastupdated = new Date();
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
          alert(err);
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
      if (!this.showUnArchivedOnly) {
        return true;
      } else {
        return item.isarchived == false;
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
    this.$emit("newHeaderTitle", "Projecten - Overzicht");
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
#showunarchivedonlyboxMobile {
  margin-top: 10px;
  color: white;
}



</style>