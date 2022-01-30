<template>
  <div oncontextmenu="return false;">

    <div>
      <div class="row">
        <h5 v-if="this.searchedNormalFolders.length > 0">Mappen</h5>
        <div v-for="folder in searchedNormalFolders" :key="folder.name" class="col-sm-4">
          <ProjectFolder
            :folderName="folder.name"
            :folderType="folder.type"
            :folderPath="folder.path"
            :projectID="folder.projectID"
            :currentFolders="this.currentFolders"
            :files="folder.files"

            @currentPathChanged="currentPathChanged"
            @folderMoved="currentFoldersChanged()"
            @folderDeleted="currentFoldersChanged()"
            @nameChanged="currentFoldersChanged()"
            @folderSelected="folderSelected(folder)"
            @folderDeselected="folderDeselected(folder)"
            
    
            @dragenter="addClass"
            @dragleave="removeClass"
            @mouseleave.self="removeClass"

            @drop="onDrop($event, folder.path)"
            @dragenter.prevent
            @dragover.prevent
            draggable="true"
            @dragstart="startDrag($event, folder.path)"
          />
        </div>
        <h5 v-if="this.searchedSharedFolders.length > 0">Gedeelde Mappen</h5>
        <div v-for="folder in searchedSharedFolders" :key="folder.name" class="col-sm-4">
          <ProjectFolder
            :folderName="folder.name"
            :folderType="folder.type"
            :folderPath="folder.path"
            :projectID="folder.projectID"
            :currentFolders="this.currentFolders"
            :files="folder.files"

            @currentPathChanged="currentPathChanged"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import ProjectFolder from "./ProjectFolder.vue";
import AlertService from "../../services/AlertService";

export default {
  setup(){
    const startDrag = (event, path) => {
      event.dataTransfer.dropEffect = 'move'
      event.dataTransfer.effectAllowed = 'move'
      event.dataTransfer.setData('path', path)
      event.dataTransfer.setData('type', 'folder')
    }

    return{
      startDrag,
    }
  },
  components: {
    ProjectFolder,
  },
  name: "FoldersView",
  props: ['projectID', 'currentPath', 'previousPath', 'currentSharedFolders', 'currentFolders', 'searchTerm'],
  computed: {
    searchedSharedFolders: function () {
      var searchedSharedFolders = []
      for(var sharedFolder of this.currentSharedFolders){
        var folderName = sharedFolder.name
        if(this.folderNameInSearchTerm(String(folderName), this.searchTerm)){
          searchedSharedFolders.push(sharedFolder)
        }
      }
      return searchedSharedFolders
    },
    searchedNormalFolders: function () {
      if(this.searchTerm == "" || this.searchTerm == null){
       return this.currentFolders;
      }
      else{
        var searchedFolders = []
        for(var folder_index in this.currentFolders){
          var folderName = this.currentFolders[folder_index].name
          if(this.folderNameInSearchTerm(String(folderName), this.searchTerm)){
            searchedFolders.push(this.currentFolders[folder_index])
          }
        }
        return searchedFolders
      }
    }
  },
  data: function () {
    return {
      searchedFolders: [],
    };
  },
  methods: {
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
              this.$emit("currentFilesChanged");
            })
            .catch((err) => {
              AlertService.handleError(err);
            });
      }
      else{
        FilestorageService.moveFolder(this.projectID, path, to, '')
            .then((response) => {
              AlertService.handleSuccess(response)
              this.$emit("currentFoldersChanged");
            })
            .catch((err) => {
              AlertService.handleError(err);
            });
      }
    },
    folderNameInSearchTerm(folderName, searchTerm) {
      return folderName.includes(searchTerm) || searchTerm == null;
    },
    folderSelected(folder){
      this.$emit("folderSelected", folder)
    },
    folderDeselected(folder){
      this.$emit("folderDeselected", folder)
    },
    currentFoldersChanged(){
      this.$emit("currentFoldersChanged")
    },
    currentPathChanged(newPath, projectID){
      this.$emit("currentPathChanged", newPath, projectID);
    }
  },
};
</script>


<style scoped>
.row {
  margin-top: 1vh;
}
.component-container{
  height: auto;
  min-height: auto;
}
</style>