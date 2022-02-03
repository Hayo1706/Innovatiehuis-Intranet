<template>
  <div>
    <ConfirmDialogue ref="confirmDialogue"></ConfirmDialogue>
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
              @change="selectUpload"
              type="file"
              id="files"
              name="files"
              multiple
              hidden
            />
            <label v-if="this.uploadMenu == true" for="files" refs="files" class="file-btn">
              <img
                title="Upload bestand"
                class="component-header-button"
                src=".\..\..\assets\images\upload_file.png"
              />
          </label>
          <div v-else title="Uploading bestanden..." class="spinner-border" role="status" alt="uploading...">
          </div>
          <img
            data-toggle="tooltip"
            data-placement="bottom"
            title="Map aanmaken"
            class="component-header-button"
            src=".\..\..\assets\images\create_folder.png"
            data-bs-toggle="modal"
            data-bs-target="#folderModal"
          />
          <img
            title="Vorige versies bestanden"
            class="component-header-button"
            @click="this.$emit('showOlderFiles')"
            src=".\..\..\assets\images\restore.png"
          />
          <div v-if="this.selectedFiles.length + this.selectedFolders.length > 0">
            <img
              @click="this.$emit('deselectSelectedElements')"
              title="Deselecteren"
              class="component-header-button"
              src=".\..\..\assets\images\cancel_selection.png"
            />
            <img
              @click="this.$emit('deleteSelectedElements')"
              title="Verwijderen"
              class="component-header-button"
              src=".\..\..\assets\images\delete.png"
            />
            <img
              v-if="this.selectedFiles.length > 0 && this.selectedFolders.length == 0"
              @click="this.$emit('shareSelectedElements')"
              title="Bestanden delen"
              class="component-header-button"
              src=".\..\..\assets\images\share_files.png"
            />
            <img
              @click="this.$emit('moveSelectedElements')"
              title="Geselecteerde elementen verplaatsen"
              class="component-header-button"
              src=".\..\..\assets\images\move_selected.png"
            />
          </div>
        </nav>
      </div>
      <div class='row' v-for="file of this.uploadingFiles" :key='file'>
        <div class='col-sm-8'>
          <h5>{{ file.name }}</h5>
        </div>
        <div class='col-sm-4'>
          <div class="progress">
            <div class="progress-bar" role="progressbar" :style="{width: file.percentage + '%'}" aria-valuemin="0" aria-valuemax="100"></div>
          </div>
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
import AlertService from "../../services/AlertService";
import ConfirmDialogue from "@/shared_components/ConfirmDialogue.vue";

export default {
  name: "ProjectFolderHeader",
  components: {
    SearchBar,
    ConfirmDialogue
  },
  props: ["currentPath", "sharedChilds", "selectedFolders", "selectedFiles", "droppedFiles"],
  data: function () {
    return {
      newFolderName: null,
      uploadMenu: true,
      files: [],
      uploadingFiles: [],
    };
  },
  watch: {
    droppedFiles: function(newFiles) {
      this.uploadFiles(newFiles)
    }
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
    selectUpload(e){
      var files = e.target.files;
      this.uploadFiles(files)
      document.getElementById("files").value = null;
    },
    updateUploadingFile(index, name, percentage){
      this.uploadingFiles[index] = {"name": name, "percentage": percentage}
    },
    async confirmAction(message){
      const confirmation = await this.$refs.confirmDialogue.show({
        title: "",
        message:
          message,
      });
      return confirmation
    },
    uploadFiles(files) {
      this.uploadMenu = false;
      var amountOfFiles = files.length;
      for (let i = 0; i < files.length; i++) {

        amountOfFiles--; 
        if(amountOfFiles == 0){
          this.uploadMenu = true;
          this.uploadingFiles = []
        }

        this.uploadingFiles.push({"name": files[i].name, "percentage": 0})
        var formData = new FormData();
        formData.append(files[i].name, files[i]);
        
        var config = { 
          onUploadProgress: function(progressEvent) {
             var percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            console.log(percentCompleted, progressEvent)
            this.uploadingFiles[i]['percentage'] = percentCompleted
          }.bind(this)
        }

        FilestorageService.uploadFile(
          this.$route.params.id,
          this.currentPath,
          formData,
          null,
          config
        )
          .then((response) => {
            AlertService.handleSuccess(response);
            this.$emit("newFilesUploaded");
          })
          .catch((err) => {
            if(err instanceof TypeError){
              this.uploadMenu = true;
              this.uploadingFiles = []
              AlertService.alert("Uw upload is mislukt! De server is weggevallen. Contacteer een van onze medewerkers.", "error")
              return;
            }
            else if(err.response.status === 409){
              console.log(err.response.data.message)
              this.confirmAction(err.response.data.message).then((confirmation) => {
              FilestorageService.uploadFile(
                this.$route.params.id,
                this.currentPath,
                formData,
                confirmation,
                config
              )
                .then((response) => {
                  if(amountOfFiles == 0){
                    this.uploadingFiles = []
                  }
                  AlertService.handleSuccess(response);
                  this.$emit("newFilesUploaded");
                })
                .catch((err) => {
                  if(amountOfFiles == 0){
                    this.uploadingFiles = []
                  }
                  else if(err instanceof TypeError){
                    this.uploadMenu = true;
                    this.uploadingFiles = []
                    AlertService.alert("Uw upload is mislukt! De server is weggevallen. Contacteer een van onze medewerkers.", "error")
                    return;
                  }
                  AlertService.handleError(err);
                });
              })
            }
            else{
              AlertService.handleError(err);
            }
          });
      }
    },
    canUploadFile() {
      return PermissionService.userHasPermission(
        "may_update_file_in_own_project"
      );
    },
  },

};
</script>
