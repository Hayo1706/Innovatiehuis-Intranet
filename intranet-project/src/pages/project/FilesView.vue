<template>
  <div>
    <div class="component-header">
        <ProjectFilesHeader
          :path="this.folderPath"
          @searchBarChanged="setSearchedFiles"
          @newFilesUploaded="currentFilesChanged"
        >
        Bestanden
        </ProjectFilesHeader>
    </div>
      <div class="row">
        <div v-for="file in searchedFiles" :key="file" class="col-sm-2">
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
import ProjectFilesHeader from "./ProjectFilesHeader.vue";
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
    ProjectFilesHeader,
    ProjectFile,
  },
  name: "FilesView",
  props: ['projectID', 'currentPath', 'sharedChilds', 'currentFolders', 'currentFiles', 'searchTerm'],
  watch: {
    searchTerm: function(){
      this.setSearchedFiles(this.searchTerm);
    },
    currentPath: function(newPath){
      this.folderPath = newPath;
    },
    currentFolders(newFolders){
      this.folders = newFolders;
    },
    currentFiles: function(){
      this.setSearchedFiles(this.searchTerm);
    }
  },
  data: function () {
    return {
      folders: [],
      searchedFiles: [],
      folderPath: this.currentPath,
    };
  },
  methods: {
    setSearchedFiles(searchTerm){
      if(searchTerm == "" || searchTerm == null){
          this.searchedFiles = this.currentFiles;  
      }
      else{
        this.searchedFiles = []
        for(var folder_index in this.currentFiles){
          var folderName = this.currentFiles[folder_index].name
          if(this.fileNameInSearchterm(String(folderName), searchTerm)){
            this.searchedFiles.push(this.currentFiles[folder_index])
          }
        }
      }
    },
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
        console.log(child.shared_files)
        if(child.projectid == childID){
          sharedFiles = child.shared_files;
        }
      }
      
      if(sharedFiles == null){
        alert(sharedFiles)
        sharedFiles = path;
      }
      else{
        sharedFiles += " " + path;
      }

      const project = {
        shared_files: sharedFiles
      }

      ProjectService.updateSharedFilesOfProject(projectID, childID, project)
      .then((response) => {
        AlertService.handleSuccess(response);
        this.$emit("currentFilesChanged")
      })
      .catch((err) => {
        AlertService.handleError(err);
      })
    },
  },
  async created(){
    this.setSearchedFiles();
  }
};
</script>

<style scoped>
.component-container{
  height: auto;
  min-height: auto;
}
</style>