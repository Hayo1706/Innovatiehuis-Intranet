<template>
  <div oncontextmenu="return false;">
    <div class="component-header">
      <ProjectFolderHeader
          :path="this.folderPath"
          @newFolderAdded="currentFoldersChanged()"
          @searchBarChanged="setSearchTerm">
          <div id="projectPath">
            <text v-if="this.folderPath == ''">Mappen</text>
          
            <text 
              @dragenter.prevent
              @dragover.prevent
              @drop="onDrop($event, '/')"
              @dragenter="addClass"
              @dragleave="removeClass"
              @mouseleave.self="removeClass"

              v-else class="hover"
              @click="currentPathChanged('', this.projectID)"
            >Home/</text>
            <span v-for="(path, index) in fullPath = this.folderPath.split('/').slice(0,-1)" :key="path">
              <text
                  @drop="onDrop($event, '/'+ fullPath.slice(1, index+1)[0])"
                  @dragenter.prevent
                  @dragover.prevent
                  @dragenter="addClass"
                  @dragleave="removeClass"
                  @mouseleave.self="removeClass"

                  class="hover"
                  @click="currentPathChanged('/'+fullPath.slice(1, index+1)[0], this.projectID)"
                  v-if="path != ''">{{ path }}/</text>
            </span>
            <text>
              {{this.folderPath.split('/').slice(-1)[0]}}
            </text>
          </div>
        </ProjectFolderHeader>
    </div>

    <div>
      <div class="row">

        <div col-sm-4>
          <ProjectFolder
          
          />
        </div>

        <div v-for="folder in searchedFolders" :key="folder.name" class="col-sm-4">
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

      </div>
    </div>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import ProjectFolderHeader from "./ProjectFolderHeader.vue";
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
    ProjectFolderHeader,
    ProjectFolder,
  },
  name: "FoldersView",
  props: ['projectID', 'currentPath', 'previousPath', 'currentFolders'],
  watch: {
    currentFolders: function(newFolders){
      this.setSearchedFolders(newFolders);
    },
    currentPath: function(newPath){
      this.folderPath = newPath;
    },
  },
  data: function () {
    return {
      errorStatus: false,
      folderPath: this.currentPath,
      searchedFolders: [],
      searchTerm: "",
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
    setSearchTerm(searchTerm) {
      this.searchTerm = searchTerm;
      this.setSearchedFolders(this.searchTerm);
    },
    folderNameInSearchTerm(folderName, searchTerm) {
      return folderName.includes(searchTerm) || searchTerm == null;
    },   
    setSearchedFolders(searchTerm){
      if(searchTerm == "" || searchTerm == null){
          this.searchedFolders = this.currentFolders;  
      }
      else{
        this.searchedFolders = []
        for(var folder_index in this.currentFolders){
          var folderName = this.currentFolders[folder_index].name
          if(this.folderNameInSearchTerm(String(folderName), this.searchTerm)){
            this.searchedFolders.push(this.currentFolders[folder_index])
          }
        }
      }
    },
    currentFoldersChanged(){
      this.$emit("currentFoldersChanged")
    },
    currentPathChanged(newPath, projectID){
      this.folderPath = newPath;
      this.$emit("currentPathChanged", newPath, projectID);
    }
  },
  async created() {
    this.setSearchedFolders();
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

#projectPath {
  overflow: hidden;
}
</style>