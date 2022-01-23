<template>
  <div>
    <div class="component-header">
        <ProjectFilesHeader
          :path="this.folderPath"
          @searchBarChanged="setSearchTerm"
          @newFilesUploaded="currentFilesChanged"
        >
        Bestanden
        </ProjectFilesHeader>
    </div>
      <div class="row">
        <div v-for="file in currentFiles" :key="file" class="col-sm-2">
          <div v-if="fileNameInSearchterm(file.name)">
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

              draggable="true"
              @dragstart="startDrag($event, file.path)"
            />
          </div>
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
  props: ['projectID', 'currentPath', 'sharedChilds', 'currentFolders', 'currentFiles'],
watch: {
    currentPath: function(newPath){
      this.folderPath = newPath;
    },
    currentFolders(newFolders){
      this.folders = newFolders;
    }
  },
  data: function () {
    return {
      folders: [],
      folderPath: this.currentPath,
      searchTerm: "",
    };
  },
  methods: {
    fileNameInSearchterm(name) {
      return name.includes(this.searchTerm) || this.searchTerm == null;
    },
    setSearchTerm(value) {
      this.searchTerm = value;
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
        this.$emit("currentFilesChanged")
        AlertService.handleSuccess(response);
      })
      .catch((err) => {
        AlertService.handleError(err);
      })
    },
  },
};
</script>

<style scoped>
.component-container{
  height: auto;
  min-height: auto;
}
</style>