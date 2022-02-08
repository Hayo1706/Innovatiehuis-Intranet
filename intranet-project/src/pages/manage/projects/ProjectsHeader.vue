<template>
  <div id="projectsHeader" class="container-fluid d-none d-lg-block">
    <div id="projects-header-top" class="row">
      <button
        id="addProject"
        class="btn pmd-btn-fab pmd-ripple-effect btn-primary"
        data-bs-toggle="modal"
        data-bs-target="#createProjectModal"
        type="button"
        v-show="canCreateProject()"
      >
      <img src="@/assets/images/plus2.png">
        Project toevoegen
      </button>
      <ProjectsShowArchivedCheckbox
        @showArchived="(value) => $emit('showArchived', value)"
        v-bind:showArchived="this.showArchived"
      />
    </div>

    <div class="row">
      <div
        class="col-3 column-title"
        @click="this.$emit('sortEvent', 'name')"
        style="position: relative"
      >
        Projectnaam
        <span v-if="sortingMethod == 'name'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>

      <div class="col column-title" @click="this.$emit('sortEvent', 'created')">
        Aangemaakt
        <span v-if="sortingMethod == 'created'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>
      <div
        class="col column-title"
        @click="this.$emit('sortEvent', 'last_updated')"
      >
        Laatst aangepast
        <span v-if="sortingMethod == 'last_updated'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>
      <div
        class="col column-title"
        @click="this.$emit('sortEvent', 'archive_status')"
      >
        Status
        <span v-if="sortingMethod == 'archive_status'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>
      <div class="col search-col">
        <SearchBar
          @searchBarChanged="
            (searchTerm) => $emit('searchBarChanged', searchTerm)
          "
          placeholder="Filter op naam..."
          v-bind:searchTerm="this.searchTerm"
          style="margin-bottom: 4px;"
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
  background: hsl(0deg 0% 98% / 90%);
  color: white;
  font-size: 1.6vh;
  padding: 11px 0 0 0;
  border-bottom: 2px solid hsl(225deg 7% 89%);
}
#search-input {
  font-family: AddeleThin;
  border-style: solid;
}
.column-title {
  font-size: 16pt;
  text-align: center;
  background: rgb(224 224 224);
  border: 1px solid #d4d4d4;
  border-bottom: 0px;
}
.column-title:hover {
  cursor: pointer;
  background: rgb(216, 216, 216);
}
img {
  filter: invert(1);
  width: 3vh;
  margin: 0 8px 4px 0;
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
#addProject {
  background-color: var(--blue2);
  width: fit-content;
  display: inline-block;
  left: 0px;
  margin-left: 13px;
  padding-bottom: 3px;
}
#addProject div{
  color: white;
}
#projects-header-top{
  padding-bottom: 11px;
  margin: 0;
}
.form-switch{
  margin-left: auto;
  display: flex;
  align-items: flex-end;
}
.input-group{
  margin: 0 !important;
}
</style>