<template>
  <div>
    <div class="row">
      <div class="col-sm-4" id="center">
        <SearchBar
          @searchBarChanged="
            (searchTerm) => $emit('searchBarChanged', searchTerm)
          "
          placeholder="Filter op naam..."
          v-bind:searchTerm="this.searchTerm"
        ></SearchBar>
      </div>
      <div class="col-sm-8">
        <nav class="mb-1 navbar navbar-expand-lg btn-blue">
          <input
              @change="uploadFiles"
              type="file"
              id="files"
              name="files"
              multiple
              hidden
            />
            <label for="files" refs="files" class="file-btn">
              <img
                title="Upload bestand"
                class="component-header-button"
                src=".\..\..\assets\images\new_upload.png"
              />
          </label>
          <img
            data-toggle="tooltip"
            data-placement="bottom"
            title="Map aanmaken"
            class="component-header-button"
            src=".\..\..\assets\images\newfolder.png"
            data-bs-toggle="modal"
            data-bs-target="#folderModal"
          />
          <img
            @click="this.$emit('deleteSelectedElements')"
            title="Verwijderen"
            class="component-header-button"
            src=".\..\..\assets\images\delete.png"
          />
          <img
            @click="this.$emit('shareSelectedElements')"
            title="Delen"
            class="component-header-button"
            src=".\..\..\assets\images\share_folder.png"
          />
          <img
            @click="this.$emit('moveSelectedElements')"
            title="Bestanden verplaatsen"
            class="component-header-button"
            src=".\..\..\assets\images\move_folder.png"
          />
          <img
            @click="this.$emit('deselectSelectedElements')"
            title="Deselecteren"
            class="component-header-button"
            src=".\..\..\assets\images\x.png"
          />
        </nav>
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
import AlertService from "../../services/AlertService";

export default {
  name: "ProjectFolderHeader",
  components: {
    SearchBar,
  },
  props: ["currentPath", "sharedChilds", "selectedFolders", "selectedFiles"],
  data: function () {
    return {
      newFolderName: null,
      files: [],
    };
  },
  methods: {
    addNewFolder() {
      if (this.newFolderName == null) {
        this.newFolderName = "Nieuwe_Map";
      }
      FilestorageService.createFolder(
        this.$route.params.id,
        this.currentPath,
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
    uploadFiles(e) {
      this.uploadMenu = false;
      var files = e.target.files;
      var amountOfFiles = files.length;
      for (let i = 0; i < files.length; i++) {
        var formData = new FormData();
        formData.append(files[i].name, files[i]);

        FilestorageService.uploadFiles(
          this.$route.params.id,
          this.currentPath,
          formData
        )
          .then((response) => {
            amountOfFiles--; 
            if(amountOfFiles == 0){
              this.uploadMenu = true;
            }
            AlertService.handleSuccess(response);
            this.$emit("newFilesUploaded");
          })
          .catch((err) => {
            amountOfFiles--; 
            if(amountOfFiles == 0){
              this.uploadMenu = true;
            }
            AlertService.handleError(err);
            if (err.response.status === 409) {
              var confirmation = confirm(err.response.data.response.message);
              FilestorageService.uploadFiles(
                this.$route.params.id,
                this.path,
                formData,
                confirmation
              )
                .then((response) => {
                  amountOfFiles--; 
                  if(amountOfFiles == 0){
                    alert()
                    this.uploadMenu = true;
                  }
                  AlertService.handleSuccess(response);
                  this.$emit("newFilesUploaded");
                })
                .catch((err) => {
                  amountOfFiles--; 
                  if(amountOfFiles == 0){
                    this.uploadMenu = true;
                  }
                  AlertService.handleError(err);
                });
            }
          });
      }
      document.getElementById("files").value = null;
    },
    canUploadFile() {
      return PermissionService.userHasPermission(
        "may_update_file_in_own_project"
      );
    },
  },

};
</script>
