<template>
  <div
    class="projectFile"
    @contextmenu="viewMenu = true"
    @long-press="viewMenu = true"
    @mouseleave="viewMenu = false; moveMenu = false"
  >
    <div class="row">
       <img :src="this.getTypeImage()" v-bind:id="this.type"/>
    </div>
     <ul v-show="canDownloadFile()" id="drop-down-menu" v-if="viewMenu == true">
          <li v-show="canRenameFile()" @click="enableInput()">Wijzig Naam</li>
          <li v-show="canMoveFile()" @click="moveMenu = true; setFolders(); viewMenu = false;">Verplaats</li>
          <li v-show="canDownloadFile()" @click="downloadFile()">Download</li>
          <li v-show="canDeleteFile()" @click="deleteFile()">Verwijder</li>
      </ul>

      <ul id="drop-down-menu" v-if="moveMenu == true">
          <li>Verplaatsen naar:</li>
          <ul id="drop-down-menu">
            <li  v-for="folder in this.folders" :key="folder"  @click="confirmMove(folder)">
              {{ folder }}
            </li>
          </ul>
      </ul>
    <div class="row">
      <input
        v-on:keyup.enter="renameFile()"
        class="fileName"
        v-model="fileName"
        v-bind:id="this.name"
        disabled
        />
    </div> 
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import PermissionService from "@/services/PermissionService.js";

export default {
  name: "ProjectFile",
  props: {
    projectid: { type: String, required: true },
    name: { type: String, required: true },
    type: { type: String, required: false },
    path: { type: String, required: true },
    directorypath: { type: String, required: true },
    shared: { type: String, required: true },
  },
  data: function () {
    return {
      viewMenu: false,
      moveMenu: false,
      fileName: this.name,
      folders: [],
      fileType: this.type,
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
      downloadFile(){
        FilestorageService.downloadFile(this.projectid, this.path)
        .then((response) => { 
          const url = window.URL.createObjectURL(new Blob([response.data]))
          const link = document.createElement('a')
          link.href = url;
          link.setAttribute('download', this.name);
          document.body.appendChild(link);
          link.click();
          link.href = window.URL.createObjectURL(new Blob());
        }).catch(console.error)
      },
      deleteFile(){
        FilestorageService.deleteFile(this.projectid, this.path)
        .then(() => {
          this.$emit("fileDeleted");
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
      },
      renameFile() {
        this.disableInput();
        var newFileName = this.fileName + "." + this.fileType
        if(this.name != newFileName && newFileName != this.name + this.type){
          FilestorageService.renameFile(this.projectid, this.path, newFileName)
            .then((response) => {
              console.log(response.data);
              this.$emit("nameChanged");
            })
            .catch((err) => {
              if (err.response) {
                this.fileName = this.name
                console.log(err.response.status);
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
      setFolders() {
        FilestorageService.getFoldersOfProject(this.projectid, this.directorypath)
          .then((response) => {
            this.folders = response;
          })
          .catch((err) => {
            if (err.response) {
              console.log(err.response.status);
            }
          });
      },
      moveFile(target_folder) {
        var target_path = this.directorypath + '/' + target_folder
        FilestorageService.moveFile(this.projectid, this.path, target_path)
        .then(() => {
            this.$emit("fileMoved");
          })
          .catch((err) => {
            if (err.response) {
              console.log(err.response.status);
            }
          });
      },
      getTypeImage() {
        var result = this.fileTypes[this.type];
        result = (typeof result !== "undefined") ? result : this.fileTypes["unknown"];
        return result
      },
      confirmMove(target_folder){
        if(confirm("Are you sure you want to move " + this.name + " to " + target_folder + "?")){
          this.moveFile(target_folder)
        }
      },
      confirmDelete(file_name){
        if(confirm("Are you sure you want to delete " + file_name + "?")){
          this.deleteFile()
        }
      },
      canDeleteFile(){
        return PermissionService.userHasPermission("may_update_file_in_own_project");
      },
      canMoveFile(){
        return PermissionService.userHasPermission("may_update_file_in_own_project");
      },
      canRenameFile(){
        return PermissionService.userHasPermission("may_update_file_in_own_project");
      },
      canDownloadFile(){
        return PermissionService.userHasPermission("may_read_own_project");
      }
  },
};
</script>

<style scoped>
.projectFile {
  color: var(--blue1);
  width: 100%;
  min-height: calc(1.5vw + 1.5vh);
  font-size: calc(0.5vh + 0.5vw);
}
.fileName {
  background-color: transparent;
  color: var(--blue1);
  border: 0px;
}
</style>