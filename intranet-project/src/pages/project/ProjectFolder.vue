<template>
  <div @mouseleave="moveMenu = false; unsetMenus();">
    <ConfirmDialogue ref="confirmDialogue"></ConfirmDialogue>
    <div
      class="projectFolder hover"
      @contextmenu="setViewMenu(this.getCoordinates())"
      @long-press="setViewMenu(this.getCoordinates())"
      @touchstart="goToFolder()"
      @dblclick="goToFolder()"
      @click.ctrl="this.selected = !this.selected; selectFolder()"
      v-bind:id="this.folderPath + 2"
    >
      <div class="container" style="padding: 0px 12px 0px 12px;pointer-events: none;">
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
              v-if="this.folderType == 'shared' || this.folderType == 'owned'"
              src=".\..\..\assets\images\shared_folder.png"
              draggable="false"
            />
          </div>
          <div class="col-8" style="display: inline-block; position: relative">
            <div style="position:absolute; left:0; right:0; top:0; bottom:0;z-index: 10" />
            <div style="display:flex;align-items:center;width:100%;height:100%;">
              <textarea
                maxlength="36"
                rows="2"
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
    <div
      v-show="canSeeMenu() && this.folderType == 'normal'"
      class="dropdown-menu dropdown-menu-sm"
      v-bind:id="this.projectID + this.folderPath"
    >
      <a class="dropdown-item" v-show="canRenameFolder()" @click="enableInput()">Wijzig Naam</a>
      <a
        class="dropdown-item"
        v-show="canMoveFolder()"
        v-if="this.currentFolders.length > 1"
        @click="moveMenu = true; setMoveMenu(this.getCoordinates())"
      >Verplaatsen naar:</a>
      <div class="dropdown-menu dropdown-menu-sm" v-bind:id="this.folderPath + 1">
        <span v-for="folder in this.currentFolders" :key="folder" @click="confirmMove(folder)">
          <a
            class="dropdown-item"
            v-if="folder.name != folderName && folder.type == 'normal'"
          >{{ folder.name }}</a>
        </span>
      </div>
      <a class="dropdown-item" v-show="canDeleteFolder()" @click="deleteFolder()">Verwijder</a>
    </div>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import PermissionService from "@/services/PermissionService.js";
import AlertService from "../../services/AlertService";
import ConfirmDialogue from "@/shared_components/ConfirmDialogue.vue";

export default {
  name: "ProjectFolder",
  props: {
    folderName: { type: String, required: true },
    folderPath: { type: String, required: true },
    folderType: { type: String, required: true },

    projectID: { type: String, required: true },
    currentFolders: { type: Array, required: true },

    files: { type: Array, required: false }
  },
  components: { ConfirmDialogue },
  data: function () {
    return {
      selected: false,
      viewMenu: false,
      moveMenu: false,
      newName: this.folderName,
      folders: [],
    };
  },
  methods: {
    selectFolder() {
      if (this.folderType == "normal") {
        var folderDiv = document.getElementById(this.folderPath + 2);
        if (this.selected == true) {
          folderDiv.style["border-width"] = "5px";
          this.$emit("folderSelected")
        }
        else {
          folderDiv.style["border-width"] = "1px";
          this.$emit("folderDeselected")
        }
      }

    },
    setMoveMenu() {
      if (this.folderType == 'normal') {
        var element = document.getElementById(this.folderPath + 1)
        element.style['display'] = 'block'
      }
    },
    setViewMenu(e) {
      if (this.folderType == 'normal') {
        var top = e.top;
        var left = e.left;
        var element = document.getElementById(this.projectID + this.folderPath)
        element.style['display'] = 'block'
        element.style['top'] = String(left) + 'px'
        element.style['left'] = String(top) + 'px'
      }
    },
    unsetMenus() {
      var viewMenu = document.getElementById(this.projectID + this.folderPath)
      viewMenu.style['display'] = 'none'
      var moveMenu = document.getElementById(this.folderPath + 1)
      moveMenu.style['display'] = 'none'
    },
    getCoordinates() {
      var e = window.event;
      var posX = e.clientX;
      var posY = e.clientY;
      return { 'top': posX, 'left': posY }
    },
    deleteFolder() {
      FilestorageService.deleteFolder(this.projectID, this.folderPath, false)
        .then((response) => {
          this.$emit("folderDeleted");
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          if (err.response.status === 409) {
            this.confirmDeleteContents()
          }
          else {
            AlertService.handleError(err);
          }
        });
    },
    async confirmDeleteContents() {
      const ok = await this.$refs.confirmDialogue.show({
        title: "Map verwijderen",
        message:
          'Deze map is niet leeg. Weet je zeker dat je ook de inhoud wilt verwijderen?',
      });
      if (ok) {
        FilestorageService.deleteFolder(this.projectID, this.folderPath, true)
          .then((response) => {
            this.$emit("folderDeleted");
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            AlertService.handleError(err);
          });
      }
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
            AlertService.handleError(err);
          });
      }
      else this.newName = this.folderName
    },
    enableInput() {
      this.unsetMenus();
      var inputName = document.getElementById(this.folderName)
      inputName.removeAttribute("disabled")
      inputName.select();
    },
    disableInput() {
      var inputName = document.getElementById(this.folderName)
      inputName.setAttribute("disabled", "")
    },
    moveToFolder(folder) {
      var targetPath = folder.path;
      FilestorageService.moveFolder(this.projectID, this.folderPath, targetPath, "")
        .then((response) => {
          this.$emit("folderMoved");
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    confirmMove(folder) {
      if (confirm("Are you sure you want to move " + this.folderName + " to " + folder.name + "?")) {
        this.moveToFolder(folder)
      }
    },
    goToFolder() {
      if (this.folderType == 'shared') {
        this.$emit("currentPathChanged", "?parent=" + this.projectID, this.projectID);
        return;
      }
      if (this.folderType == 'owned') {
        this.$emit("currentPathChanged", "?child=" + this.projectID, this.projectID);
        return;
      }
      this.$emit("currentPathChanged", this.folderPath, this.projectID);
    },
    canDeleteFolder() {
      return PermissionService.userHasPermission("may_update_file_in_own_project");
    },
    canMoveFolder() {
      return PermissionService.userHasPermission("may_update_file_in_own_project");
    },
    canRenameFolder() {
      return PermissionService.userHasPermission("may_update_file_in_own_project");
    },
    canSeeMenu() {
      return PermissionService.userHasPermission("may_update_file_in_own_project");
    },
  },
};
</script>

<style scoped>
#drop-down-menu {
  background: #fafafa;
  border: 1px solid var(--blue1);
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
.projectFolder {
  background-color: rgba(255, 255, 255, 0.7);
  color: var(--blue1);
  width: 100%;
  border: solid;
  border-radius: 10px;
  border-width: 1px;
  margin-top: 1vh;
  transition: 0.3s;
}
.projectFolder:hover {
  background-image: linear-gradient(
    to bottom right,
    rgba(84, 84, 218, 0.315),
    rgba(255, 255, 255, 0.7)
  );
  border-radius: 10px;
  transition: 0.3s;
}
.container {
  position: relative;
}
.foldersImage {
  margin: 8px auto;
  top: 50%;
  width: max(80%, 30px);
}
.folderName {
  position: absolute;
  background-color: transparent;
  color: var(--blue1);
  border: 0px;
  width: 90%;
  resize: none;
}
</style>