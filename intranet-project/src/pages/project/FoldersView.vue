<template>
  <div>
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
              @click="currentPathChanged('')"
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
                  @click="currentPathChanged('/'+fullPath.slice(1, index+1)[0])"
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

        <div v-for="folder in searchedFolders" :key="folder" class="col-sm-4">
          <ProjectFolder
            :folderName="folder.name"
            :folderType="folder.type"
            :folderPath="folder.path"
            :projectID="folder.projectID"
            :currentFolders="this.currentFolders"
            :currentPath="this.folderPath"
            :previousPath="this.previousPath"

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
  props: ['projectID', 'currentPath', 'previousPath', 'currentFolders', 'sharedParents'],
  watch: {
    currentFolders: function(newFolders){
      console.log("huh", newFolders)
      this.setSearchedFolders(newFolders);
    },
    currentPath: function(newPath){
      this.folderPath = newPath;
    },
    sharedParents: function(newFolders){
      this.allSharedParents = newFolders
      console.log('shared', this.allSharedParents)
    }
  },
  data: function () {
    return {
      errorStatus: false,
      folderPath: this.currentPath,
      allSharedParents: this.sharedParents,
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
            .then(() => {
              this.$emit("currentFoldersChanged");
            })
            .catch((err) => {
              if (err.response) {
                console.log(err.response.status);
              }
            });
      }
      else{
        FilestorageService.moveFolder(this.projectID, path, to, '')
            .then(() => {
              this.$emit("currentFoldersChanged");
            })
            .catch((err) => {
              if (err.response) {
                console.log(err.response.status);
              }
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
        console.log(this.currentFolders)
        for(var folder_index in this.currentFolders){
          var folderName = this.currentFolders[folder_index].name
          console.log(folderName, this.searchTerm)
          if(this.folderNameInSearchTerm(String(folderName), this.searchTerm)){
            this.searchedFolders.push(this.currentFolders[folder_index])
          }
        }
      }
    },
    currentFoldersChanged(){
      this.$emit("currentFoldersChanged")
    },
    currentPathChanged(newPath){
      this.folderPath = newPath;
      this.$emit("currentPathChanged", newPath);
    }
  },
  async created() {
    this.currentFoldersChanged();
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