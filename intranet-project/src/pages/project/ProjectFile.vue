<template>
  <div
    v-bind:title="this.path"
    v-bind:id="this.path"
    oncontextmenu="return false;"
    class="projectFile"
    @contextmenu="setViewMenu(this.getCoordinates())"
    @long-press="setViewMenu(this.getCoordinates())"
    @mouseleave="moveMenu = false; unsetMenus();
    moveMenu = false;
    shareMenu = false;"
  >
    <ConfirmDialogue ref="confirmDialogue"></ConfirmDialogue>
    <div class="row"
      @click.ctrl="this.selected = !this.selected; selectFile()"
      >
      <div class="col s10">
        <img
            draggable="false"
            class="fileImage"
            :src="this.getTypeImage()"
            v-bind:id="this.fileType"/>
        <input
          style="width: 100%"
          v-on:keydown.enter="renameFile()"
          class="fileName"
          v-model="fileName"
          v-bind:id="this.name"
          draggable="false"
          disabled
        />
      </div>
    </div>
    
    <div class="dropdown-menu dropdown-menu-sm" v-bind:id="this.projectID+this.path">
      <a class="dropdown-item" v-if="this.type == 'normal'" v-show="canUpdateFile()" @click="enableInput()">Wijzig Naam</a>
      <a class="dropdown-item" v-if="this.type == 'owned'" v-show="canUpdateFile()" @click="stopSharingFile()">Stoppen met delen</a>
      <a class="dropdown-item" v-show="canUpdateFile() && this.currentFolders.length > 1 && this.type == 'normal'" @click="setMoveMenu()">Verplaatsen naar:</a>
      <div v-show="canUpdateFile()" class="dropdown-menu dropdown-menu-sm" v-bind:id="this.path+1">
        <span v-for="folder in this.currentFolders" :key="folder"  @click="confirmMove(folder)">
          <a class="dropdown-item" v-if="folder.type == 'normal'">{{ folder.name }}</a>
        </span>
      </div>

      <a class="dropdown-item" v-if="this.type == 'normal'" v-show="canUpdateFile() && this.sharedChilds.length > 0" @click="setShareMenu()">  Delen met:</a>
      <div class="dropdown-menu dropdown-menu-sm" v-bind:id="this.path+'shareMenu'">
        <span v-for="child of this.sharedChilds" :key="child">
          <a class="dropdown-item" @click="this.confirmShare(child.project_name, child.projectid)">{{ child.project_name }}</a>
        </span>
      </div>

      <a class="dropdown-item" v-if="this.type == 'normal'" v-show="canUpdateFile()" @click="setRecoverMenu()">         Vorige versie</a>
      <div class="dropdown-menu dropdown-menu-sm" v-if="this.type == 'normal'" v-bind:id="this.path+'recoverMenu'">
        <a class="dropdown-item" v-if="this.type == 'normal'" v-show="canUpdateFile()" @click="this.confirmRecover()">      Herstellen</a>
        <a class="dropdown-item" v-if="this.type == 'normal'" v-show="canUpdateFile()" @click="downloadFile('archive')">Downloaden</a>
      </div>
      <a class="dropdown-item" v-if="this.type == 'normal'" v-show="canUpdateFile()" @click="confirmDelete()">             Verwijder</a>
      <a class="dropdown-item" v-if="this.type == 'normal' || this.type == 'shared'" v-show="canSeeFile()" @click="downloadFile('active')">      Download</a>
      <a class="dropdown-item" v-if="this.type == 'backup'" v-show="canUpdateFile()" @click="downloadFile('archive')">  Download</a>
      <a class="dropdown-item" v-if="this.type == 'backup'" v-show="canUpdateFile()" @click="this.confirmRecover()">        Herstellen</a>
    </div>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import ConfirmDialogue from "@/shared_components/ConfirmDialogue.vue";
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
  components: { ConfirmDialogue },
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
    async decryptFile(file){
      var encryptedBlob = new Blob([file])
      var encryptedFile = new File([encryptedBlob], name)
      console.log(encryptedFile)
      let iv = new Uint8Array([99, 99, 99, 99]);
      let algorithm = {
          name: "AES-GCM",
          iv: iv
      }
      let key = await crypto.subtle.importKey(
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
      let data = await encryptedBlob.arrayBuffer();
      const result = await crypto.subtle.decrypt(algorithm, key, data)
      var decryptedBlob = new Blob([result])
      return decryptedBlob
    },
    async downloadFile(version){
      FilestorageService.downloadFile(this.projectID, this.path, version)
      .then((response) => { 
        this.decryptFile(response.data)
        .then((decryptedFile) => {
          const url = window.URL.createObjectURL(decryptedFile)
          const link = document.createElement('a')
          link.href = url;
          link.setAttribute('download', this.name);
          document.body.appendChild(link);
          link.click();
          link.href = window.URL.createObjectURL(new Blob());
        })
        .catch(() => {
          AlertService.alert("Er is iets fout gegaan bij het downloaden van dit bestand, probeer het opnieuw of contacteer een medewerker.", "error")
        })
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
    async confirmAction(title, message){
      const confirmation = await this.$refs.confirmDialogue.show({
        title: title,
        message: message,
      });
      return confirmation
    },
    enableInput(){
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
          this.$emit("fileMoved");
          AlertService.handleSuccess(response);
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
        this.$emit("fileMoved");
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
    async confirmMove(targetFolder){
      if(await this.confirmAction('Verplaats bestand', "Weet je zeker dat je " + this.name + " wilt verplaatsen naar " + targetFolder.name + "?")){
        this.moveFile(targetFolder)
      }
    },
    async confirmDelete(){
      if(await this.confirmAction('Verwijder bestand', "Weet je zeker dat je " + this.name + " wilt verwijderen?")){
        this.deleteFile()
      }
    },
    async confirmShare(childName, childID){
      if(await this.confirmAction('Deel bestand', 'Weet je zeker dat je ' + this.name + ' wilt delen met ' + childName + '?')){
        this.addSharingFile(childID)
      }
    },
    async confirmRecover(){
      var element = document.getElementById(this.projectID+this.path)
      element.style['display'] = 'none'
      if(await this.confirmAction('Bestand herstellen', 'Weet je zeker dat je een vorige versie van ' + this.name + ' wilt herstellen?')){
        this.recoverBackupFile();
      }
    },
    setMoveMenu() {
      if(this.type == 'normal'){
        var element = document.getElementById(this.path+1)
        if(element.style['display'] == 'block'){
          element.style['display'] = 'none'
        }
        else{
          element.style['display'] = 'block'
        }
      }
    },
    setShareMenu() {
      if(this.type == 'normal'){
        var element = document.getElementById(this.path+'shareMenu')
        if(element.style['display'] == 'block'){
          element.style['display'] = 'none'
        }
        else{
          element.style['display'] = 'block'
        }
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
      var element = document.getElementById(this.path+"recoverMenu")
      if(element.style['display'] == 'block'){
          element.style['display'] = 'none'
        }
        else{
          element.style['display'] = 'block'
        }
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
    canUpdateFile() {
      return PermissionService.userHasPermission("may_update_file_in_own_project");
    },
    canSeeFile() {
      return PermissionService.userHasPermission("may_read_own_project");
    },
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
  width: min(50%, 150px);
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