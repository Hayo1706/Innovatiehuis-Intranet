<template>
  <div
    v-bind:id="this.path"
    oncontextmenu="return false;"
    class="projectFile"
    @contextmenu="setViewMenu(this.getCoordinates())"
    @long-press="setViewMenu(this.getCoordinates())"
    @mouseleave="moveMenu = false; unsetMenus();
    moveMenu = false;
    shareMenu = false"
  >
    <div class="row"
      @click.shift="this.selected = !this.selected; selectFile()">
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
    
    <div class="dropdown-menu dropdown-menu-sm" v-bind:id="this.projectID+this.path">
      <a class="dropdown-item" v-if="this.type == 'normal'" v-show="canRenameFile()" @click="enableInput()">Wijzig Naam</a>
      <a class="dropdown-item" v-if="this.type == 'owned'" @click="stopSharingFile()">Stoppen met delen</a>
      <a class="dropdown-item" v-show="canMoveFile()" v-if="this.currentFolders.length > 1" @click="setMoveMenu(this.getCoordinates())">Verplaatsen naar:</a>
      <div class="dropdown-menu dropdown-menu-sm" v-bind:id="this.path+1">
        <span v-for="folder in this.currentFolders" :key="folder"  @click="confirmMove(folder)">
          <a class="dropdown-item" v-if="folder.type == 'normal'">{{ folder.name }}</a>
        </span>
      </div>

      <a class="dropdown-item" v-if="this.currentFolders.length > 1" @click="setShareMenu()">Delen met:</a>
      <div class="dropdown-menu dropdown-menu-sm" v-bind:id="this.path+'shareMenu'">
        <span v-for="child of this.sharedChilds" :key="child"  @click="addSharingFile(child.projectid); unsetMenus()">
          <a class="dropdown-item">{{ child.project_name }}</a>
        </span>
      </div>
      <a class="dropdown-item" v-if="this.type != 'owned'" v-show="canDownloadFile()" @click="setRecoverMenu()">Vorige versie</a>
      <div class="dropdown-menu dropdown-menu-sm" v-bind:id="this.path+'recoverMenu'">
        <a class="dropdown-item" @click="recoverBackupFile">Herstellen</a>
        <a class="dropdown-item" @click="downloadFile('backup')">Downloaden</a>
      </div>
      <a class="dropdown-item" v-if="this.type == 'normal'" v-show="canDeleteFile()" @click="deleteFile()">Verwijder</a>
      <a class="dropdown-item" v-if="this.type != 'owned'" v-show="canDownloadFile()" @click="downloadFile('active')">Download</a>
    </div>
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
      selected: false,
      viewMenu: false,
      moveMenu: false,
      shareMenu: false,
      recoverMenu: false,
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
    selectFile(){
      if(this.type == "normal"){
        var fileDiv = document.getElementById(this.path);
        if(this.selected == true){
          fileDiv.style["border-width"] = "5px";
          this.$emit("fileSelected")
        }
        else{
          fileDiv.style["border-width"] = "1px";
          this.$emit("fileDeselected")
        }
      }
    },
    stopSharingFile(){
      this.$emit("stopSharingFile", this.path, this.projectID)
    },
    addSharingFile(childID){
      this.$emit("addSharingFile", this.path, this.projectID, childID)
    },
    downloadFile(version){
      FilestorageService.downloadFile(this.projectID, this.path, version)
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
      this.unsetMenus();
      this.fileName = this.name.split(".")[0]
      var inputName = document.getElementById(this.name)
      inputName.removeAttribute("disabled")
      inputName.select();
    },
    disableInput(){
      var inputName = document.getElementById(this.name)
      inputName.setAttribute("disabled", "")
    },
    moveFile(target_folder) {
      var target_path = target_folder.path
      FilestorageService.moveFile(this.projectID, this.path, target_path)
        .then((response) => {
          AlertService.handleSuccess(response);
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
    recoverBackupFile() {
      FilestorageService.recoverFile(this.projectID, this.path)
      .then((response) => {
        AlertService.handleSuccess(response)
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
    setMoveMenu() {
      if(this.type == 'normal'){
        var element = document.getElementById(this.path+1)
        element.style['display'] = 'block'
      }
    },
    setShareMenu() {
      if(this.type == 'normal'){
        var element = document.getElementById(this.path+'shareMenu')
        element.style['display'] = 'block'
      }
    },
    setViewMenu(e) {
      var top = e.top;
      var left = e.left;
      var element = document.getElementById(this.projectID+this.path)
      element.style['display'] = 'block'
      element.style['top'] = String(left) + 'px'
      element.style['left'] = String(top) + 'px'
    },
    setRecoverMenu() {
      var recoverMenu = document.getElementById(this.path+"recoverMenu")
      recoverMenu.style['display'] = 'block'
    },
    unsetMenus(){
      var shareMenu = document.getElementById(this.path+"shareMenu")
      shareMenu.style['display'] = 'none'
      var viewMenu = document.getElementById(this.projectID+this.path)
      viewMenu.style['display'] = 'none'
      var moveMenu = document.getElementById(this.path+1)
      moveMenu.style['display'] = 'none'
      var recoverMenu = document.getElementById(this.path+"recoverMenu")
      recoverMenu.style['display'] = 'none'
    },
    getCoordinates(){
      var e = window.event;
      var posX = e.clientX;
      var posY = e.clientY;
      return {'top':posX, 'left':posY}
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
    },
    canSeeMenu(){
        return PermissionService.userHasPermission("may_update_file_in_own_project");
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