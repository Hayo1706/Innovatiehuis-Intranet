<template>
  <div
    class="projectFolder"
    @mousemove="set_coordinates"
    @contextmenu="viewMenu = true"
    @long-press="viewMenu = true"
    @mouseleave="viewMenu = false; moveMenu = false"
  >
    <div class="container-fluid"  @click="goToFolder()">
      <div class="row">
        <div class="col-3">
          <img
            class="foldersImage"
            v-if="this.shared != 'yes'"
            src=".\..\..\assets\images\folder.png"
          />
          <img
            class="foldersImage"
            v-if="this.shared == 'yes'"
            src=".\..\..\assets\images\shared_folder.png"
          />
        </div>
        <div class="col-9">
          <input
            v-on:keyup.enter="renameFolder()"
            class="folderName"
            v-model="newName"
            v-bind:id="this.name"
            disabled
          />
        </div>
      </div>
    </div>

    <ul v-show="canSeeMenu()" id="drop-down-menu" v-if="viewMenu == true">
        <li v-show="canRenameFolder()" @click="enableInput()">Wijzig Naam</li>
        <li v-show="canMoveFolder()" v-if="this.folders.length > 0" @click="moveMenu = true; getFolders(); viewMenu = false;">Verplaats</li>
        <li v-show="canDeleteFolder()" @click="deleteFolder()">Verwijder</li>
    </ul>

    <ul v-show="canSeeMenu()" id="drop-down-menu" v-if="moveMenu == true">
        <li>Verplaatsen naar:</li>
        <ul id="drop-down-menu">
          <li  v-for="folder in this.folders" :key="folder"  @click="confirmMove(folder)">
            {{ folder }}
          </li>
        </ul>
    </ul>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import PermissionService from "@/services/PermissionService.js";

export default {
  name: "ProjectFolder",
  props: {
    projectid: { type: String, required: true },
    name: { type: String, required: true },
    path: { type: String, required: true },
    shared: { type: String, required: true },
    directorypath: { type: String, required: true },
  },
  data: function () {
    return {
      viewMenu: false,
      moveMenu: false,
      folderName: this.name,
      newName: this.name,
      folders: [],
      x: '0px',
      y: '0px'
    };
  },
  methods: {
    deleteFolder() {
      FilestorageService.deleteFolder(this.projectid, this.path, false)
        .then(() => {
          this.$emit("folderDeleted");
        })
        .catch((err) => {
          if(err.response.status === 409){
            if(confirm("There are elements within this folder, are you sure?")){
              FilestorageService.deleteFolder(this.projectid, this.path, true)
              .then(() => {
                this.$emit("folderDeleted");
              })
              .catch((err) => {
                  if (err.response) {
                    console.log(err.response);
                }
              });
              console.log(err.response.status)
            }
            console.log(err.response.status)
          }

          if (err.response) {
            console.log(err.response);
          }
        });
    },
    set_coordinates(e){
      this.x = String(e.x)
      this.y = String(e.y)
    },
    renameFolder() {
      this.disableInput();
      if (!(this.newName == this.folderName) || this.newName == '') {
        FilestorageService.renameFolder(
          this.projectid,
          this.path,
          "",
          this.newName
        )
          .then(() => {
            this.folderName = this.newName;
          })
          .catch((err) => {
            if (err.response) {
              console.log(err.response.status);
            }
          });
          this.$emit("nameChanged");
      }
      else this.newName = this.folderName
    },
    enableInput(){
      var inputName = document.getElementById(this.name)
      inputName.removeAttribute("disabled")
      inputName.select();
      this.viewMenu = false;
    },
    disableInput(){
      var inputName = document.getElementById(this.name)
      inputName.setAttribute("disabled", "")
    },
    moveToFolder(folder) {
      var folder_path = this.directorypath + "/" + folder;
      FilestorageService.moveFolder(this.projectid, this.path, folder_path, "")
        .then((response) => {
          if (response.status == 400) {
            alert(response);
          }
          this.$emit("folderMoved");
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    confirmMove(folder){
      if(confirm("Are you sure you want to move " + this.name + " to " + folder + "?")){
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
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    goToFolder() {
      this.$emit("currentPathChanged", this.directorypath + "/" + this.folderName);
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

<style>
.projectFolder {
  color: var(--blue1);
  width: 100%;
  min-height: calc(1.5vw + 1.5vh);
  font-size: calc(0.5vh + 0.5vw);
}
.foldersImage {
  width: calc(1.5vw + 1.5vh);
}
.folderName {
  background-color: transparent;
  color: var(--blue1);
  border: 0px;
}
.container {
  margin-top: 2vh;
}
h5 {
  color: black;
}
#drop-down-menu{
    background: #FAFAFA;
    border: 1px solid var(--blue1);
    display: block;
    list-style: none;
    margin: 0;
    padding: 0;
    position: absolute;
    width: 250px;
    z-index: 999999;
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
</style>