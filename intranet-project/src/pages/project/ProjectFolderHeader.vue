<template>
  <div>
    <div id="projectFolderHeader">
      <div class="row">
        <div class="col-sm-8">
          <slot></slot>
        </div>
        <div class="col-sm-3">
          <SearchBar
            @searchBarChanged="
              (searchTerm) => $emit('searchBarChanged', searchTerm)
            "
            placeholder="Filter op naam..."
            v-bind:searchTerm="this.searchTerm"
          ></SearchBar>
        </div>

        <div class="col-sm-1">
          <img
            data-toggle="tooltip"
            data-placement="bottom"
            title="Map aanmaken"
            class="component-header-button"
            src=".\..\..\assets\images\newfolder.png"
            data-bs-toggle="modal"
            data-bs-target="#folderModal"
            v-if="canAddFolder()"
          />
        </div>
      </div>
    </div>

    
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import PermissionService from "@/services/PermissionService.js";
import SearchBar from "@/shared_components/SearchBar.vue";
import AlertService from "../../services/AlertService";

export default {
  name: "ProjectFolderHeader",
  components: {
    SearchBar,
  },
  props: ["path"],
  data: function () {
    return {
      newFolderName: null,
    };
  },
  methods: {
    addNewFolder() {
      if (this.newFolderName == null) {
        this.newFolderName = "Nieuwe_Map";
      }
      FilestorageService.createFolder(
        this.$route.params.id,
        this.path,
        this.newFolderName
      )
        .then((response) => {
          this.$emit("newFolderAdded");
          this.newFolderName = null;
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    canAddFolder() {
      return PermissionService.userHasPermission(
        "may_update_file_in_own_project"
      );
    },
  },
};
</script>
