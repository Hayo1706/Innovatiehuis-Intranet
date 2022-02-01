<template>
  <div @dragover.prevent @drop.prevent>
    <h5 class="directory-view-title">Bestanden</h5>
      <div class="row" style="min-height: 15vh" @drop="uploadFile" @dragover="toggleDropZone(true)" @dragleave="toggleDropZone(false)" id="drop_zone">
        <div v-for="file in this.searchedFiles" :key="file" class="col-sm-2">
          <ProjectFile
            :projectID="file.projectID"
            :name="file.name"
            :fileType="file.name.split('.').pop()"
            :path="file.path"
            :type="file.type"
            :currentFolders="this.currentFolders"
            :currentFiles="this.currentFiles"
            :sharedChilds="this.sharedChilds"

            @fileDeleted="currentFilesChanged"
            @nameChanged="currentFilesChanged"
            @fileMoved="currentFilesChanged"
            
            @stopSharingFile="stopSharingFile"
            @addSharingFile="addSharingFile"

            @fileSelected="this.$emit('fileSelected', file)"
            @fileDeselected="this.$emit('fileDeselected', file)"

            draggable="true"
            @dragstart="startDrag($event, file.path)"
          />
        </div>
      </div>
  </div>
</template>

<script>
import ProjectFile from "./ProjectFile.vue";
import AlertService from "../../services/AlertService";
import ProjectService from "../../services/ProjectService";

export default {
  setup(){
    const startDrag = (event, path) => {
      event.dataTransfer.dropEffect = 'move'
      event.dataTransfer.effectAllowed = 'move'
      event.dataTransfer.setData('path', path)
      event.dataTransfer.setData('type', 'file')
    }

    return{
      startDrag,
    }
  },
  components: {
    ProjectFile,
  },
  name: "FilesView",
  props: ['projectID', 'currentPath', 'sharedChilds', 'currentFolders', 'currentFiles', 'searchTerm'],
  computed: {
    searchedFiles: function() {
      if(this.searchTerm == "" || this.searchTerm == null){
          return this.currentFiles;  
      }
      else{
        var searchedFiles = []
        for(var file_index in this.currentFiles){
          var folderName = this.currentFiles[file_index].name.toLowerCase();
          if(this.fileNameInSearchterm(String(folderName), this.searchTerm.toLowerCase())){
            searchedFiles.push(this.currentFiles[file_index])
          }
        }
        return searchedFiles;
      }
    }
  },

  data: function () {
    return {
      folders: [],
    };
  },
  methods: {
    fileNameInSearchterm(name, searchTerm) {
      return name.includes(searchTerm) || searchTerm == null;
    },
    currentFilesChanged(){
      this.$emit("currentFilesChanged")
    },
    stopSharingFile(path, projectID){
      var sharedFiles = []
      for(var file of this.currentFiles){
        if(file.projectID == projectID && file.type == 'owned'){
          if(path != file.path){
            sharedFiles.push(file.path)
          }
        }
      }
      if(sharedFiles.length > 0){
        this.$emit("sharedFilesChanged", sharedFiles.join(" "))
      }
      else{
        this.$emit("sharedFilesChanged", null)
      }
    },
    addSharingFile(path, projectID, childID){
      var sharedFiles = ""
      for(var child of this.sharedChilds){
        if(child.projectid == childID){
          sharedFiles = child.shared_files;
        }
      }
      
      if(sharedFiles == null){
        sharedFiles = path;
      }
      else if(!sharedFiles.split(" ").includes(path)){
        sharedFiles += " " + path;
      }

      const project = {
        shared_files: sharedFiles
      }

      ProjectService.updateSharedFilesOfProject(projectID, childID, project)
      .then((response) => {
        console.log(response)
        AlertService.handleSuccess(response);
        this.$emit("currentFilesChanged")
      })
      .catch((err) => {
        console.log(err)
        AlertService.handleError(err);
      })
    },
    uploadFile(e){
      this.toggleDropZone(false)
      var files = e.dataTransfer.files
      if(files.length > 0){
        this.$emit("filesDropUpload", files)
      }
    },
    toggleDropZone(showBoolean) {
      var dropZone = document.getElementById("drop_zone")
      if(showBoolean == true){
        dropZone.style['background-color'] = "var(--blue4)";
      }
      else{
        dropZone.style['background-color'] = "transparent"
      }
    },
  },
};
</script>

<style>
.component-container{
  height: auto;
  min-height: auto;
}
</style>