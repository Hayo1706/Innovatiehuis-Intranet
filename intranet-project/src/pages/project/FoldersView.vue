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
          <div v-if="folderNameInSearchTerm(folder)">
            <ProjectFolder
              :folderName="folder"
              :folderType="'normal'"
              :folderPath="this.folderPath + '/' + folder"
              :projectID="this.projectID"
              :currentFolders="this.currentFolders"
              :currentPath="this.folderPath"
              :previousPath="this.previousPath"

              @currentPathChanged="currentPathChanged"
              @folderMoved="currentFoldersChanged()"
              @folderDeleted="currentFoldersChanged()"
              @nameChanged="currentFoldersChanged()"
              
      
              @dragenter="addClass"
              @dragleave.self="removeClass"
              @mouseleave.self="removeClass"

              @drop="onDrop($event, this.folderPath + '/' + folder)"
              @dragenter.prevent
              @dragover.prevent
              draggable="true"
              @dragstart="startDrag($event, this.folderPath + '/' + folder)"
            />
          </div>
        </div>

        <div v-for="parent in allSharedParents" :key="parent" class="col-sm-4">
          <div v-if="folderNameInSearchTerm(parent['project_name'])">
            <ProjectFolder
              :folderName="parent['project_name']"
              :folderType="'shared'"
              :folderPath="this.folderPath + '?parent=' + parent['projectid']"
              :projectID="parent['projectid']"
              :currentFolders="this.currentFolders"
              :currentPath="this.folderPath + '?parent=' + parent['projectid']"
              :previousPath="this.folderPath"

              @currentPathChanged="currentPathChanged"
              @folderMoved="currentFoldersChanged()"
              @folderDeleted="currentFoldersChanged()"
              @nameChanged="currentFoldersChanged()"
            />
          </div>
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
    currentFolders: function(){
      this.setSearchedFolders();
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
      this.setSearchedFolders();
    },
    folderNameInSearchTerm(folderName, searchTerm) {
      return folderName.includes(searchTerm) || searchTerm == null;
    },   
    setSearchedFolders(){
      console.log("test",this.currentFolders)
      if(this.searchTerm == "" || this.searchTerm == null){
          this.searchedFolders = this.currentFolders;  
      }
      else{
        this.searchedFolders = []
        for(var folder_index in this.currentFolders){
          if(this.folderNameInSearchTerm(this.currentFolders[folder_index], this.searchTerm)){
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