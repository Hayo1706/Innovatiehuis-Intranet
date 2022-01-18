<template>
  <div id="projectsHeader" class="container-fluid d-none d-lg-block">
    <div id="projects-header-top" class="row">
      <ProjectsHideArchivedCheckbox
        @hideArchived="(value) => $emit('hideArchived', value)"
        v-bind:hideArchived="this.hideArchived"
    />
    </div>
    
    <div class="row">
      <div class="full-button col-3" @click="this.$emit('sortEvent', 'name')">
        Project
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
          v-bind:searchTerm="this.searchTerm"
        ></SearchBar>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from "@/shared_components/SearchBar.vue";
import ProjectsHideArchivedCheckbox from "./ProjectsHideArchivedCheckbox.vue";
export default {
  components: { SearchBar, ProjectsHideArchivedCheckbox },
  name: "ProjectsHeader",
  props: ["searchTerm", "hideArchived", "sortingMethod", "ascending"],
  data: function () {
    return {};
  },
  methods: {},
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
.full-button {
  height: fit-content;
}
#projectsHeader .full-button{
 margin: 0;
}
</style>