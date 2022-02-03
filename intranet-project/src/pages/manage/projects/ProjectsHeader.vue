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
      <img class="plus-icon">
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
  border-bottom: 2px solid #3b3b3b;
}
#search-input {
  margin-right: 4px;
  font-family: AddeleThin;
}
.column-title {
  font-size: 16pt;
  text-align: center;
  background: rgb(204, 204, 204);
  border-radius: 2vh 2vh 0 0;
  border: 1px solid #646464;
  border-bottom: 0px;
}
.column-title:hover {
  cursor: pointer;
  background: rgb(224, 224, 224);
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
.search-col {
  padding: 0 4px;
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
.plus-icon{
  background-image: url("data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8' standalone='no' %3F%3E%3C!DOCTYPE svg PUBLIC '-//W3C//DTD SVG 1.1//EN' 'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd'%3E%3Csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' version='1.1' width='500' height='500' viewBox='0 0 500 500' xml:space='preserve'%3E%3Cdesc%3ECreated with Fabric.js 4.6.0%3C/desc%3E%3Cdefs%3E%3C/defs%3E%3Cg transform='matrix(1 0 0 1 250 250)' id='Z2y7PqTuZ6nO58Ds8PCRy' %3E%3Cpath style='stroke: rgb(209,11,249); stroke-width: 0; stroke-dasharray: none; stroke-linecap: butt; stroke-dashoffset: 0; stroke-linejoin: miter; stroke-miterlimit: 4; fill: rgb(255,255,255); fill-rule: nonzero; opacity: 1;' vector-effect='non-scaling-stroke' transform=' translate(-250, -250)' d='M 202.93837 0 L 297.06164 0 L 297.06164 202.5 L 500 202.5 L 500 297.5 L 297.06164 297.5 L 297.06164 500 L 202.93837000000002 500 L 202.93837000000002 297.5 L 2.842170943040401e-14 297.5 L 2.842170943040401e-14 202.5 L 202.93837000000002 202.5 z' stroke-linecap='round' /%3E%3C/g%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  height: 100%;
}

</style>