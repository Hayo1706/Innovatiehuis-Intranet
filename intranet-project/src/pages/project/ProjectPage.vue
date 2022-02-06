<template>
  <div>
    <div id="ProjectPage" class="container-fluid">
      <div class="row">
        <div class="col-sm-9">
          <div class="component-container">
            <div class="component-header" style="overflow: visible;">
              <text
                class="directory"
                @dragenter.prevent
                @dragover.prevent
                @drop="onDrop($event, '/')"
                @dragenter="addClass"
                @dragleave="removeClass"
                @mouseleave.self="removeClass"
                
                @click="currentPathChanged('', this.projectID)"
              >{{ this.projectName }}</text>
              <span v-for="(path, index) in this.currentPath.split('/').slice(1)" :key="path">
                /
                <text
                  class="directory"
                  @click="currentPathChanged('/' + this.currentPath.split('/').slice(1, index + 2).join('/'), this.projectID)"
                  v-if="path != ''"
                >{{ path }}</text>
              </span>
              <text v-if="this.childID != null"> / {{ "Gedeeld met: " + this.getChildName() }}</text>
              <text v-if="this.parentID != null"> / {{ "Gedeeld door: " + this.getParentName() }}</text>

              <ProjectPageHeader
                :currentPath="this.currentPath"
                :sharedChilds="this.sharedChilds"
                :selectedFolders="this.selectedFolders"
                :selectedFiles="this.selectedFiles"
                :droppedFiles="this.droppedFiles"
                :currentFolders="this.currentFolders"
                :currentFiles="this.currentFiles"
                :projectID="this.projectID"

                @newFolderAdded="currentFoldersChanged()"
                @newFilesUploaded="currentFilesChanged()"
                @elementsMoved="currentFilesChanged(); currentFoldersChanged();"
                @showOlderFiles="togglePreviousFilesMenu()"
                @deleteSelectedElements="deleteSelectedElements()"
                @moveSelectedElements="moveSelectedElements()"
                @deselectSelectedElements="resetSelectedElements()"
                @shareSelectedElements="shareSelectedFiles()"
                @searchBarChanged="setSearchTerm"
              ></ProjectPageHeader>
            </div>
            <div class="scrollable">
              <FoldersView
                  :previousPath="this.previousPath"
                  :currentPath="this.currentPath"
                  :projectID="this.projectID"
                  :currentFolders="this.currentFolders"
                  :currentSharedFolders="this.currentSharedFolders"
                  :searchTerm="this.searchTerm"

                  @currentFoldersChanged="currentFoldersChanged"
                  @currentFilesChanged="currentFilesChanged"
                  @currentPathChanged="currentPathChanged"
                  @folderSelected="selectFolder"
                  @folderDeselected="deselectFolder"
                  @fileMoved="currentFilesChanged"
               />
               <FilesView 
                ref="child" 
                :currentPath="this.currentPath"
                :projectID="this.projectID"
                :currentFolders="this.currentFolders"
                :currentFiles="this.currentFiles"
                :olderFiles="this.olderFiles"
                :previousFilesMenu="this.previousFilesMenu"
                :sharedChilds="this.sharedChilds"
                :searchTerm="this.searchTerm"

                @sharedFilesChanged="sharedFilesChanged"
                @currentFilesChanged="currentFilesChanged"
                @fileSelected="selectFile"
                @fileDeselected="deselectFile"
                @filesDropUpload="setFilesDropUpload"
              />
            </div>
          </div>
        </div>
        <div class="col-sm-3">
            <AnnouncementWindow
              @reload="reloadAnnouncementWindow()"
              :key="this.announcementWindowKey"
              >Mededelingen</AnnouncementWindow
            >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilesView from "./FilesView.vue";
import FoldersView from "./FoldersView.vue";
import ProjectPageHeader from "./ProjectPageHeader.vue";
import AnnouncementWindow from "../../shared_components/AnnouncementWindow.vue";
import AlertService from "../../services/AlertService";
import ProjectService from "../../services/ProjectService.js";
import FilestorageService from "../../services/FilestorageService.js";

export default {
  components: { FilesView, FoldersView, AnnouncementWindow, ProjectPageHeader },
  name: "ProjectPage",
  data: function () {
    return {
      announcementWindowKey: 0,

      projectID: this.getProjectId(),
      projectName: "",
      parentID: this.$route.query.parent,
      childID: this.$route.query.child,
      toolMenu: false,
      previousFilesMenu: false,
      olderFiles: [],
      droppedFiles: null,

      searchTerm: "",

      previousPath: "",
      currentPath: this.getPath(),
      currentFiles: [],
      currentFolders: [],
      currentSharedFolders: [],

      sharedChilds: [],
      sharedParents: [],

      selectedFolders: [],
      selectedFiles: [],
    };
  },
  setup() {
    const startDrag = (event, path) => {
      event.dataTransfer.dropEffect = 'move'
      event.dataTransfer.effectAllowed = 'move'
      event.dataTransfer.setData('path', path)
      event.dataTransfer.setData('type', 'folder')
    }

    return {
      startDrag,
    }
  },
  watch: {
    $route() {
      if (this.$route.fullPath.includes("/project/")) {
        this.childID = this.$route.query.child;
        this.parentID = this.$route.query.parent;
        this.currentPath = this.getPath();
        this.previousPath = this.getPreviousPath(this.$route.path)
        this.resetSelectedElements();
        this.setParentProjects();
        this.setChildProjects();
        this.setCurrentFolders();
        this.setCurrentFiles();
      }
    },
  },
  methods: {
    togglePreviousFilesMenu() {
      this.previousFilesMenu = !this.previousFilesMenu
      if (this.previousFilesMenu == true) {
        if (this.parentID == null && this.childID == null) {
          FilestorageService.getOlderFiles(this.projectID)
            .then((response) => {
              this.olderFiles = []
              for (var file in response.data) {
                this.olderFiles.push({ 'name': response.data[file].split("\\").pop(), 'path': response.data[file].split("\\").join("/"), 'projectID': this.projectID, 'type': 'backup' })
              }
              AlertService.handleSuccess(response);
            })
            .catch((err) => {
              AlertService.handleError(err);
            });
        }
      }
    },
    setFilesDropUpload: function (fileList) {
      this.droppedFiles = fileList
    },
    addClass: function (e) {
      if (e.target.classList.contains("hover"))
        e.target.classList.add("hoverDrag");
    },
    removeClass: function (e) {
      if (e.target.classList.contains("hover"))
        e.target.classList.remove("hoverDrag");
    },
    onDrop(event, to) {
      const path = event.dataTransfer.getData('path')
      let id = this.projectID
      if (to === path)
        return
      if (event.dataTransfer.getData('type') === 'file') {
        FilestorageService.moveFile(id, path, to)
          .then((response) => {
            AlertService.handleSuccess(response)
            this.setCurrentFiles();
          })
          .catch((err) => {
            AlertService.handleError(err);
          });
      }
      else {
        FilestorageService.moveFolder(this.projectID, path, to, '')
          .then((response) => {
            AlertService.handleSuccess(response)
            this.setCurrentFolders();
          })
          .catch((err) => {
            AlertService.handleError(err);
          });
      }
    },
    resetSelectedElements() {
      this.selectedFolders = []
      this.selectedFiles = []
    },
    getPreviousPath(currentPath) {
      var previousPath = "/" + currentPath.split("/project/" + this.projectID)[1].split("/").slice(1, -1).join("/")
      if (previousPath == "/") {
        return ""
      }
      return previousPath
    },
    getChildName() {
      for (var child of this.sharedChilds) {
        if (child.projectid == this.childID) {
          return child.project_name
        }
      }
      return this.childID
    },
    getParentName() {
      for (var parent of this.sharedParents) {
        if (parent.projectid == this.parentID) {
          return parent.project_name
        }
      }
      return this.parentID
    },
    async deleteSelectedFolders() {
      for (var folder of this.selectedFolders) {
        await FilestorageService.deleteFolder(this.projectID, folder.path, false)
          .then((response) => {
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            if (err.response.status === 409) {
              if (confirm("There are elements in " + folder.name + ", are you sure you want to delete it?")) {
                FilestorageService.deleteFolder(this.projectID, folder.path, true)
                  .then((response) => {
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
      }
    },
    async deleteSelectedFiles() {
      for (var file of this.selectedFiles) {
        await FilestorageService.deleteFile(this.projectID, file.path)
          .then((response) => {
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            AlertService.handleError(err);
          });
      }
    },
    async deleteSelectedElements() {
      if (this.selectedElementsNotNull()) {
        await this.deleteSelectedFolders().then(() => {
          this.currentFoldersChanged();
        }).then(() => {
          this.deleteSelectedFiles().then(() => {
            this.currentFilesChanged();
          }).then(() => {
            this.resetSelectedElements();
          })
        })
      }
    },
    async moveSelectedElements() {
      if (this.selectedElementsNotNull()) {
        await this.moveSelectedFolders().then(() => {
          this.currentFoldersChanged();
        }).then(() => {
          this.moveSelectedFiles().then(() => {
            this.currentFilesChanged();
          }).then(() => {
            this.resetSelectedElements();
          })
        })
      }
    },
    async moveSelectedFiles(targetFolder) {
      for (var file of this.selectedFiles) {
        await FilestorageService.moveFile(this.projectID, file.path, targetFolder.path)
          .then((response) => {
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            AlertService.handleError(err);
          });
      }
    },
    async moveSelectedFolders(targetFolder) {
      for (var folder of this.selectedFolders) {
        await FilestorageService.moveFolder(this.projectID, folder.path, targetFolder.path, "")
          .then((response) => {
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            AlertService.handleError(err);
          });
      }
      this.selectedFolders = []
    },
    async shareSelectedFiles(childID) {
      this.setChildProjects();
      var newSharedFiles = ""
      for (var child in this.sharedChilds) {
        if (child.projectid == childID) {
          newSharedFiles = child.shared_files
        }
      }
      for (var file of this.selectedFiles) {
        newSharedFiles += " " + file.path
      }
      newSharedFiles
    },
    selectedElementsNotNull() {
      return this.selectedFolders.length > 0 || this.selectedFiles.length > 0
    },
    selectFolder(folder) {
      this.selectedFolders.push(folder)
    },
    deselectFolder(folder) {
      for (var folderIndex in this.selectedFolders) {
        if (folder.path == this.selectedFolders[folderIndex].path) {
          this.selectedFolders.splice(folderIndex, 1)
        }
      }
    },
    selectFile(file) {
      this.selectedFiles.push(file)
    },
    deselectFile(file) {
      for (var fileIndex in this.selectedFiles) {
        if (file.path == this.selectedFiles[fileIndex].path) {
          this.selectedFiles.splice(fileIndex, 1)
        }
      }
    },
    currentFoldersChanged() {
      this.setCurrentFolders();
      this.selectedFolders = [];
    },
    currentFilesChanged() {
      this.setChildProjects();
      this.togglePreviousFilesMenu();
      this.setParentProjects();
      this.setCurrentFiles();
      this.selectedFiles = [];
    },
    sharedFilesChanged(sharedFiles) {
      const project = {
        shared_files: sharedFiles
      }
      ProjectService.updateSharedFilesOfProject(this.projectID, this.childID, project)
        .then((response) => {
          this.setCurrentFiles();
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        })
    },
    currentPathChanged(path, familyID) {
      this.projectID = this.getProjectId();
      this.previousPath = this.currentPath;
      this.$router.push("/project/" + this.projectID + path);

      if (this.projectID == familyID) {
        this.parentID = null;
        this.childID = null;
        this.currentPath = path
      }
      else {
        this.currentPath = ""
        if (path.includes("child")) {
          this.childID = familyID
        }
        else if (path.includes("parent")) {
          this.parentID = familyID
        }
      }
    },
    reloadAnnouncementWindow() {
      this.announcementWindowKey += 1;
    },
    getPath() {
      return this.$route.path.split("/project/")[1].split(this.$route.params.id)[1]
    },
    getProjectId() {
      return this.$route.params.id
    },
    setSearchTerm(searchTerm) {
      this.searchTerm = searchTerm;
    },
    setCurrentFolders() {
      this.currentFolders = []
      this.currentSharedFolders = []
      if (this.parentID == null && this.childID == null) {
        FilestorageService.getFoldersOfProject(this.projectID, this.currentPath)
          .then((response) => {
            for (var folder in response.data) {
              this.currentFolders.push({ 'name': response.data[folder], 'path': this.currentPath + '/' + response.data[folder], 'projectID': this.projectID, 'type': 'normal' })
            }
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            AlertService.handleError(err);
          });
        if (this.currentPath == '') {
          this.setParentFolders();
          this.setChildFolders();
        }
      }
      return this.currentFolders
    },
    setChildFolders() {
      ProjectService.getChildrenById(this.projectID)
        .then((response) => {
          for (var child in response.data.result) {
            var childName = response.data.result[child].project_name
            var childID = response.data.result[child].projectid
            this.currentSharedFolders.push({ 'name': "Gedeeld met:\n" + childName, 'path': '/', 'projectID': childID, 'type': 'owned' })
          }
        })
        .catch((err) => {
          AlertService.handleError(err)
        })
    },
    setParentFolders() {
      ProjectService.getParentsById(this.projectID)
        .then((response) => {
          for (var parent in response.data.result) {
            var parentID = response.data.result[parent].projectid
            var parentName = response.data.result[parent].project_name
            this.currentSharedFolders.push({ 'name': "Gedeeld door:\n" + parentName, 'path': '/', 'projectID': parentID, 'type': 'shared' })
          }
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        })
    },
    setCurrentFiles() {
      this.currentFiles = []
      if (this.parentID == null && this.childID == null) {
        FilestorageService.getFilesOfPath(this.projectID, this.currentPath)
          .then((response) => {
            this.currentFiles = []
            for (var file in response.data) {
              this.currentFiles.push({ 'name': response.data[file], 'path': this.currentPath + '/' + response.data[file], 'projectID': this.projectID, 'type': 'normal' })
            }
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            AlertService.handleError(err);
          });
      }
      else {
        if (this.parentID != null) {
          this.setParentFiles();
        }
        else {
          this.setChildFiles();
        }
      }
      return this.currentFiles
    },
    setParentFiles() {
      ProjectService.getParentsById(this.projectID)
        .then((response) => {
          for (var parent of response.data.result) {
            var parentID = parent.projectid
            if (this.parentID == parentID) {
              var sharedFiles = parent.shared_files.split(" ")
              for (var file in sharedFiles) {
                var fileName = sharedFiles[file].split("/").pop()
                this.currentFiles.push({ 'name': fileName, 'path': sharedFiles[file], 'projectID': parentID, 'type': 'shared' })
              }
            }
          }
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        })
    },
    setParentProjects() {
      this.sharedParents = []
      ProjectService.getParentsById(this.projectID)
        .then((response) => {
          for (var parent of response.data.result) {
            this.sharedParents.push(parent)
          }
        })
        .catch((err) => {
          AlertService.handleError(err);
        })
    },
    setChildFiles() {
      ProjectService.getChildrenById(this.projectID)
        .then((response) => {
          for (var child of response.data.result) {
            var childID = child.projectid
            if (childID == this.childID) {
              var sharedFiles = child.shared_files.split(" ")
              for (var file of sharedFiles) {
                var fileName = file.split("/").pop()
                this.currentFiles.push({ 'name': fileName, 'path': file, 'projectID': this.projectID, 'type': 'owned' })
              }
            }
          }
        })
        .catch((err) => {
          AlertService.handleError(err)
        })
    },
    setProjectName() {
      ProjectService.getProjectById(this.$route.params.id)
        .then((response) => {
          this.projectName = response.data.result[0].project_name;
          this.$emit("newHeaderTitle", response.data.result[0].project_name);
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    setChildProjects() {
      this.sharedChilds = []
      ProjectService.getChildrenById(this.projectID)
        .then((response) => {
          for (var child of response.data.result) {
            this.sharedChilds.push(child)
          }
        })
        .catch((err) => {
          AlertService.handleError(err)
        })
    }
  },
  async created() {
    this.previousPath = this.getPreviousPath(this.$route.path)
    this.setProjectName();
    this.setChildProjects();
    this.setParentProjects();

    this.setCurrentFolders();
    this.setCurrentFiles();
  },
};
</script>

<style>
.directory {
  cursor: pointer;
}
.directory:hover {
  color:var(--gold1);
}
.scrollable {
  overflow: scroll;
  height: 70vh;
}

</style>