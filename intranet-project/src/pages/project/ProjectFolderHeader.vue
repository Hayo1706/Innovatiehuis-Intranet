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
            v-bind:searchTerm="this.searchTerm"
          ></SearchBar>
        </div>

        <div class="col-sm-1">
          <img
            data-toggle="tooltip" data-placement="bottom" title="Map aanmaken"
            class="component-header-button"
            src=".\..\..\assets\images\newfolder.png" 
            data-bs-toggle="modal"
            data-bs-target="#folderModal"
            v-if="canAddFolder()"
          />
        </div>
      </div>
    </div>

    <div
      class="modal fade"
      id="folderModal"
      tabindex="-1"
      aria-labelledby="folderModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="folderModalLabel">
              Nieuwe map aanmaken
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-9">
                <input
                  v-model="this.newFolderName"
                  class="form-control"
                  id="message-text"
                  placeholder="Nieuwe_Map"
                />
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-primary"
              data-bs-dismiss="modal"
              @click="addNewFolder()"
            >
              Toevoegen
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Annuleren
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import PermissionService from "@/services/PermissionService.js";
import SearchBar from "@/shared_components/SearchBar.vue";
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
        .then(() => {
          this.$emit("newFolderAdded");
          this.newFolderName = null;
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    canAddFolder(){
      return PermissionService.userHasPermission("may_update_file_in_own_project");
    }
  },
};
</script>
