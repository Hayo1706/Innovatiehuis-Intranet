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
            title="Verwijderde bestanden terughalen"
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
            <div class="dropdown">
              <img
                v-if="this.selectedFiles.length > 0 && this.selectedFolders.length == 0"
                title="Bestanden delen"
                class="component-header-button"
                src=".\..\..\assets\images\share_files.png"
              />
              <div class="dropdown-content">
                <a>Delen met:</a>
                <a v-for="child in this.sharedChilds" :key="child" @click="shareSelectedFiles(child.projectid, child.shared_files)">{{ child.project_name }}</a>
              </div>
            </div>
            <div class="dropdown">
              <img
                title="Geselecteerde elementen verplaatsen"
                class="component-header-button"
                src=".\..\..\assets\images\move_selected.png"
              />
              <div class="dropdown-content">
                <a>Verplaatsen naar:</a>
                <a v-for="folder in this.currentFolders" :key="folder"  @click="moveSelectedElements(folder).then(() => {this.$emit('elementsMoved');} )">{{ folder.name }}</a>
              </div>
            </div>
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
                  v-on:keydown.enter="addNewFolder()"
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
import ProjectService from '../../services/ProjectService';

export default {
  name: "ProjectFolderHeader",
  components: {
    SearchBar,
    ConfirmDialogue
  },
  props: ["projectID", "currentPath", "currentFolders", "sharedChilds", "selectedFolders", "selectedFiles", "droppedFiles"],
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
    async moveSelectedElements(folder){
      var targetPath = folder.path
      for(var file of this.selectedFiles){
        FilestorageService.moveFile(this.projectID, file.path, targetPath)
        .then(() => {
        })
        .catch((err) => {
          AlertService.handleError(err)
        });
      }
      for(var selectedFolder of this.selectedFolders){
        FilestorageService.moveFolder(this.projectID, selectedFolder.path, targetPath, "")
        .then(() => {
          this.$emit("folderMoved")
        })
        .catch((err) => {
          AlertService.handleError(err);
        })
      }
    },
    shareSelectedFiles(childID, sharedFiles){
      var newSharedFiles = sharedFiles
      for(var file of this.selectedFiles){
        if(newSharedFiles == null){
          newSharedFiles = file.path
        }
        else if(!sharedFiles.split(" ").includes(file.path)){
          newSharedFiles += " " + file.path
        }
      }
      const project = {
        shared_files: newSharedFiles
      }

      ProjectService.updateSharedFilesOfProject(this.projectID, childID, project)
      .then((response) => {
        AlertService.handleSuccess(response);
        this.$emit("currentFilesChanged")
      })
      .catch((err) => {
        AlertService.handleError(err);
      })
    },
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
    async uploadFiles(files) {
      this.uploadMenu = false;
      var amountOfFiles = files.length;
      for (let i = 0; i < files.length; i++) {

        var blob = files[i]
        var name = files[i].name
        
        let iv = new Uint8Array([99, 99, 99, 99]);
        
        let algorithm = {
            name: "AES-GCM",
            iv: iv
        }

        let newKey = await crypto.subtle.importKey(
            "jwk", 
            {   
                kty: "oct",
                k: "Y0zt37HgOx-BY7SQjYVmrqhPkO44Ii2Jcb9yydUDPfE",
                alg: "A256GCM",
                ext: true,
            },
            {   
                name: "AES-GCM",
            },
            true, 
            ["encrypt", "decrypt"] 
        )

        let data = await blob.arrayBuffer();
        const result = await crypto.subtle.encrypt(algorithm, newKey, data)
        var fileBlob = new Blob([result])
        var encryptedFile = new File([fileBlob], name)

        amountOfFiles--; 
        if(amountOfFiles == 0){
          this.uploadMenu = true;
          this.uploadingFiles = []
        }

        this.uploadingFiles.push({"name": name, "percentage": 0})
        var formData = new FormData();
        formData.append(name, encryptedFile);
        
        var config = { 
          onUploadProgress: function(progressEvent) {
             var percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
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
<style scoped>
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  font-size: 16px;
}

.dropdown-content a:hover {background-color: #ddd;}

.dropdown:hover .dropdown-content {display: block;}

.dropdown:hover .dropbtn {background-color: #3e8e41;}
</style>