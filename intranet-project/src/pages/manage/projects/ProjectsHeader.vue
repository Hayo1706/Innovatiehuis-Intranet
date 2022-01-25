<template>
  <div id="projectsHeader" class="container-fluid d-none d-lg-block">
    <div id="projects-header-top" class="row">
      <button
        id="actionButton"
        class="btn pmd-btn-fab pmd-ripple-effect btn-primary"
        data-bs-toggle="modal"
        data-bs-target="#createProjectModal"
        type="button"
        v-show="canCreateProject()"
      >
        <i class="material-icons pmd-sm">Project toevoegen</i>
      </button>
      <ProjectsShowArchivedCheckbox
        @showArchived="(value) => $emit('showArchived', value)"
        v-bind:showArchived="this.showArchived"
      />
    </div>

    <div class="row">
      <div
        class="full-button col-3"
        @click="this.$emit('sortEvent', 'name')"
        style="position: relative"
      >
        Projectnaam
        <span v-if="sortingMethod == 'name'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>

      <div class="full-button col" @click="this.$emit('sortEvent', 'created')">
        Aangemaakt
        <span v-if="sortingMethod == 'created'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>
      <div
        class="full-button col"
        @click="this.$emit('sortEvent', 'last_updated')"
      >
        Laatst aangepast
        <span v-if="sortingMethod == 'last_updated'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>
      <div
        class="full-button col"
        @click="this.$emit('sortEvent', 'archive_status')"
      >
        Archiveerstatus
        <span v-if="sortingMethod == 'archive_status'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>
      <div class="col">
        <SearchBar
          @searchBarChanged="
            (searchTerm) => $emit('searchBarChanged', searchTerm)
          "
          placeholder="Filter op naam..."
          v-bind:searchTerm="this.searchTerm"
        ></SearchBar>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from "@/shared_components/SearchBar.vue";
import ProjectsShowArchivedCheckbox from "./ProjectsShowArchivedCheckbox.vue";
import PermissionService from "@/services/PermissionService.js";
export default {
  components: { SearchBar, ProjectsShowArchivedCheckbox },
  name: "ProjectsHeader",
  props: ["searchTerm", "showArchived", "sortingMethod", "ascending"],
  data: function () {
    return {};
  },
  methods: {
    canCreateProject() {
      return PermissionService.userHasPermission("may_create_project");
    },
  },
};
</script>

<style scoped>
#projectsHeader {
  width: 100%;
  box-sizing: border-box;
  min-height: 5vh;
  background-color: var(--blue1);
  color: white;
  font-size: 1.6vh;
  padding: 11px 0 0 0;
}
#search-input {
  margin-right: 4px;
  font-family: AddeleThin;
}
img {
  width: calc(2vw + 3vh);
  padding-bottom: 10px;
  padding-left: 10px;
  cursor: pointer;
}
.bi-caret-down-fill {
  margin-left: 5px;
}
.bi-caret-up-fill {
  margin-left: 5px;
}
.col {
  font-family: AddeleSemiBold;
}
#projectsHeader .full-button {
  margin: 0;
}
#actionButton {
  width: fit-content;
  display: inline-block;
  left: 0px;
  margin-left: 13px;
}
#projects-header-top{
  padding-bottom: 11px;
  margin: 0;
}
.form-switch{
  margin-left: auto;
  display: flex;
  align-items: end;
}

</style>