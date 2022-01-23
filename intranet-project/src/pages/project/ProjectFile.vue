<template>
  <div
    class="projectFile"
    @contextmenu="viewMenu = true"
    @long-press="viewMenu = true"
    @mouseleave="viewMenu = false;
    moveMenu = false;
    shareMenu = false"
  >
    <div class="row">
      <div class="col s10">
        <img
            draggable="false"
            class="fileImage"
            :src="this.getTypeImage()"
            v-bind:id="this.fileType"/>
        <input
          v-on:keyup.enter="renameFile()"
          class="fileName"
          v-model="fileName"
          v-bind:id="this.name"
          draggable="false"
          disabled
        />
      </div>
    </div>

    <ul v-show="canDownloadFile()" id="drop-down-menu" v-if="viewMenu == true">
      <li v-if="this.type == 'normal'" v-show="canRenameFile()" @click="enableInput()">Wijzig Naam</li>
      <li v-if="this.type == 'normal'" v-show="canMoveFile()" @click="moveMenu = true; viewMenu = false;">Verplaats</li>
      <li v-if="this.type == 'normal'" @click="shareMenu = true; viewMenu = false">Delen</li>
      <li v-if="this.type == 'owned'" @click="stopSharingFile()">Delen Stoppen</li>
      <li v-show="canDownloadFile()" @click="downloadFile()">Download</li>
      <li v-if="this.type == 'normal'" v-show="canDeleteFile()" @click="deleteFile()">Verwijder</li>
    </ul>
    <ul id="drop-down-menu" v-if="moveMenu == true && this.shared != 'no'">
      <li>Verplaatsen naar:</li>
      <ul id="drop-down-menu">
        <span v-for="folder in this.currentFolders" :key="folder"  @click="confirmMove(folder)">
            <li v-if="folder.name != folderName && folder.type != 'shared'">
              {{ folder.name }}
            </li>
          </span>
      </ul>
    </ul>
    <ul id="drop-down-menu" v-if="shareMenu == true">
      <li>Delen met:</li>
      <ul id="drop-down-menu">
        <span v-for="child in this.sharedChilds" :key="child"  @click="addSharingFile(child.projectid)">
            <li>
              {{ child.project_name }}
            </li>
          </span>
      </ul>
    </ul>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import PermissionService from "@/services/PermissionService.js";
import AlertService from "../../services/AlertService";

export default {
  name: "ProjectFile",
  props: {
    projectID: { type: String, required: true },
    name: { type: String, required: true },
    fileType: { type: String, required: false },
    path: { type: String, required: true },
    type: { type: String, required: true },
    currentFolders: { type: Array, required: true },
    currentFiles: { type: Array, required: true },
    sharedChilds: { type: Array, required: false }
  },
  data: function () {
    return {
      viewMenu: false,
      moveMenu: false,
      shareMenu: false,
      fileName: this.name,
      fileTypes: {
        jpg: require("./../../assets/images/file_icons/Jpg.png"),
        jpeg: require("./../../assets/images/file_icons/Jpeg.png"),
        png: require("./../../assets/images/file_icons/Png.png"),
        pdf: require("./../../assets/images/file_icons/Pdf.png"),
        docx: require("./../../assets/images/file_icons/Word.png"),
        xlsx: require("./../../assets/images/file_icons/Excel.png"),
        pptx: require("./../../assets/images/file_icons/PowerPoint.png"),
        txt: require("./../../assets/images/file_icons/Text.png"),
        unknown: require("./../../assets/images/file_icons/Unknown.png"),
      },
    };
  },
  methods: {
    stopSharingFile(){
      this.$emit("stopSharingFile", this.path, this.projectID)
    },
    addSharingFile(childID){
      this.$emit("addSharingFile", this.path, this.projectID, childID)
    },
    downloadFile(){
      FilestorageService.downloadFile(this.projectID, this.path)
      .then((response) => { 
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url;
        link.setAttribute('download', this.name);
        document.body.appendChild(link);
        link.click();
        link.href = window.URL.createObjectURL(new Blob());
      })
      .catch((err) => {
        AlertService.handleError(err);
      });
    },

    renameFile() {
      this.disableInput();
      var newFileName = this.fileName + "." + this.fileType
      if(this.name != newFileName && newFileName != this.name + this.fileType){
        FilestorageService.renameFile(this.projectID, this.path, newFileName)
          .then(() => {
            this.$emit("nameChanged");
          })
          .catch((err) => {
            if (err.response) {
              this.fileName = this.name
              AlertService.handleError(err);
            }
          });
      }
      else{
        this.fileName = this.name
      }
    },
    enableInput(){
      this.fileName = this.name.split(".")[0]
      var inputName = document.getElementById(this.name)
      inputName.removeAttribute("disabled")
      this.viewMenu = false;
      inputName.select();
    },
    disableInput(){
      var inputName = document.getElementById(this.name)
      inputName.setAttribute("disabled", "")
    },
    moveFile(target_folder) {
      var target_path = target_folder.path
      FilestorageService.moveFile(this.projectID, this.path, target_path)
        .then(() => {
          this.$emit("fileMoved");
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    deleteFile() {
      FilestorageService.deleteFile(this.projectID, this.path)
        .then((response) => {
          this.$emit("fileDeleted");
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    getTypeImage() {
      var result = this.fileTypes[this.fileType];
      result = (typeof result !== "undefined") ? result : this.fileTypes["unknown"];
      return result
    },
    confirmMove(targetFolder){
      if(confirm("Are you sure you want to move " + this.name + " to " + targetFolder.name + "?")){
        this.moveFile(targetFolder)
      }
    },
    confirmDelete(file_name){
      if(confirm("Are you sure you want to delete " + file_name + "?")){
        this.deleteFile()
      }
    },
    canDeleteFile() {
      return PermissionService.userHasPermission("may_update_file_in_own_project");
    },
    canMoveFile() {
      return PermissionService.userHasPermission("may_update_file_in_own_project");
    },
    canRenameFile() {
      return PermissionService.userHasPermission("may_update_file_in_own_project");
    },
    canDownloadFile() {
      return PermissionService.userHasPermission("may_read_own_project");
    }
  },
};
</script>

<style scoped>
.projectFile {
  color: var(--blue1);
  width: 100%;
  border: solid;
  border-radius: 10px;
  border-width: 1px;
  margin-top: 1vh;
  transition: 0.3s;
}
.row {
  margin: 0;
}
.fileName {
  background-color: transparent;
  color: var(--blue1);
  border: 0;
  width: 90%;
  pointer-events: none;
}
.fileImage {
  margin: 0 auto;
  display: block;
  overflow: hidden;
  width: min(80%, 150px);
}
.projectFile:hover {
  background: white;
  border-radius: 10px;
  transition: 0.3s;
}

#drop-down-menu {
  background: #fafafa;
  border: 1px solid var(--blue1);
  display: block;
  list-style: none;
  margin: 0;
  padding: 0;
  position: absolute;
  width: 250px;
  z-index: 99;
}

#drop-down-menu li {
  border-bottom: 1px solid #e0e0e0;
  margin: 0;
  padding: 5px 35px;
}

#drop-down-menu li:last-child {
  border-bottom: none;
}

#drop-down-menu li:hover {
  background: var(--blue3);
  color: #fafafa;
}
</style>