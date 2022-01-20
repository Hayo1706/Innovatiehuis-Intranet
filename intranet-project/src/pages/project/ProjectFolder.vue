<template>
  <div
    @mouseleave="viewMenu = false; moveMenu = false"
  >
    <div
      class="projectFolder hover"
      @mousemove="set_coordinates"
      @contextmenu="viewMenu = true"
      @long-press="viewMenu = true"
      @click="goToFolder()"
    >
      <div class="container" style="padding: 0px 12px 0px 12px;pointer-events: none;"  >
        <div class="row">
          <div class="col-4">
            <img
              class="foldersImage"
              v-if="this.folderType == 'normal'"
              src=".\..\..\assets\images\folder.png"
              draggable="false"
            />
            <img
              class="foldersImage"
              v-if="this.folderType == 'goback'"
              src=".\..\..\assets\images\goback.png"
              draggable="false"
            />
            <img
              class="foldersImage"
              v-if="this.folderType == 'shared'"
              src=".\..\..\assets\images\shared_folder.png"
              draggable="false"
            />
          </div>
          <div class="col-8" style="display: inline-block; position: relative">
            <div style="position:absolute; left:0; right:0; top:0; bottom:0;z-index: 10"/>
            <div style="display:flex;align-items:center;width:100%;height:100%;">
              <input
                v-on:keyup.enter="renameFolder()"
                class="folderName"
                v-model="newName"
                v-bind:id="this.folderName"
                disabled
                draggable="false"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <ul v-show="canSeeMenu() && this.folderType ==  'normal'" id="drop-down-menu" v-if="viewMenu == true">
        <li v-show="canRenameFolder()" @click="enableInput()">Wijzig Naam</li>
        <li v-show="canMoveFolder()" v-if="this.currentFolders.length > 1" @click="moveMenu = true; viewMenu = false;">Verplaats</li>
        <li v-show="canDeleteFolder()" @click="deleteFolder()">Verwijder</li>
    </ul>

    <ul v-show="canSeeMenu()" id="drop-down-menu" v-if="moveMenu == true">
        <li>Verplaatsen naar:</li>
        <ul id="drop-down-menu">
          <span v-for="folder in this.currentFolders" :key="folder"  @click="confirmMove(folder)">
            <li v-if="folder.name != folderName && folder.type != 'shared'">
              {{ folder.name }}
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
  name: "ProjectFolder",
  props: {
    folderName: { type: String, required: true },
    folderPath: { type: String, required: true },
    folderType: { type: String, required: true },

    projectID: { type: String, required: true },
    currentFolders: { type: Array, required: true },

    files: { type: Array, required: false}
  },
  data: function () {
    return {
      viewMenu: false,
      moveMenu: false,
      newName: this.folderName,
      folders: [],
    };
  },
  methods: {
    deleteFolder() {
      FilestorageService.deleteFolder(this.projectID, this.folderPath, false)
        .then(() => {
          this.$emit("folderDeleted");
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          if(err.response.status === 409){
            if(confirm("There are elements within this folder, are you sure?")){
              FilestorageService.deleteFolder(this.projectID, this.folderPath, true)
              .then(() => {
                this.$emit("folderDeleted");
                AlertService.handleSuccess(response);
              })
              .catch((err) => {
                AlertService.handleError(err);
              });
            }
          }
          if (err.response) {
            AlertService.handleError(err);
          }
        });
    },
    renameFolder() {
      this.disableInput();
      if (!(this.newName == this.folderName) || this.newName == '') {
        FilestorageService.renameFolder(
          this.projectID,
          this.folderPath,
          "",
          this.newName
        )
        .then(() => {
          this.$emit("nameChanged");
        })
        .catch((err) => {
          this.newName = this.folderName
          if (err.response) {
            console.log(err.response.status);
          }
        });
      }
      else this.newName = this.folderName
    },
    enableInput(){
      var inputName = document.getElementById(this.folderName)
      inputName.removeAttribute("disabled")
      inputName.select();
      this.viewMenu = false;
    },
    disableInput(){
      var inputName = document.getElementById(this.folderName)
      inputName.setAttribute("disabled", "")
    },
    moveToFolder(folder) {
      var targetPath = folder.path;
      console.log(targetPath, this.folderPath, this.projectID)
      FilestorageService.moveFolder(this.projectID, this.folderPath, targetPath, "")
        .then((response) => {
          this.$emit("folderMoved");
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    confirmMove(folder){
      if(confirm("Are you sure you want to move " + this.folderName + " to " + folder.name + "?")){
        this.moveToFolder(folder)
      }
    },
    getFolders() {
      FilestorageService.getFoldersOfProject(this.projectid, this.directorypath)
        .then((response) => {
          this.folders = []
          for(var folder in response){
            if(response[folder] != this.name){
              this.folders.push(response[folder])
            }
          }
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    goToFolder() {
      if(this.files != null){
        this.$emit("currentPathChanged", "?parent=" + this.projectID, this.projectID);
        return;
      }
      this.$emit("currentPathChanged", this.folderPath, this.projectID);
    },
    canDeleteFolder(){
    return PermissionService.userHasPermission("may_update_file_in_own_project");
    },
    canMoveFolder(){
      return PermissionService.userHasPermission("may_update_file_in_own_project");
    },
    canRenameFolder(){
      return PermissionService.userHasPermission("may_update_file_in_own_project");
    },
    canSeeMenu(){
      return PermissionService.userHasPermission("may_update_file_in_own_project");
    },
  },
  async created() {
    //this.$emit("newHeaderTitle", "NAAM + PAD");
    this.getFolders();
  },
};
</script>

<style scoped>
#drop-down-menu{
    background: #FAFAFA;
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
    border-bottom: 1px solid #E0E0E0;
    margin: 0;
    padding: 5px 35px;
}

#drop-down-menu li:last-child {
    border-bottom: none;
}

#drop-down-menu li:hover {
    background: var(--blue3);
    color: #FAFAFA;
}
.projectFolder {
 color: var(--blue1);
  width: 100%;
  border: solid;
  border-radius: 10px;
  border-width: 1px;
  margin-top: 1vh;
  transition: .3s
}
.container {
  position: relative;
}
.foldersImage {
  margin:8px auto;
  top: 50%;
  overflow: hidden;
  width: max(80%, 30px);
}
.folderName {
  position: absolute;
  background-color: transparent;
  color: var(--blue1);
  border: 0px;
  width: 100%;
}
</style>