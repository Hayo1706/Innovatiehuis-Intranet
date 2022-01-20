<template>
  <div>
    <div class="component-header">
      <ProjectFolderHeader
          :path="this.currentPath"
          @newFolderAdded="(id) => setFolders()"
          @searchBarChanged="setSearchTerm">
          <div id="projectPath">
            <text v-if="this.path == ''">Mappen</text>
            <text
                @dragenter.prevent
                @dragover.prevent
                @drop="onDrop($event, '/')"
                @dragenter="addClass"
                @dragleave="removeClass"
                @mouseleave.self="removeClass"
                class="hover"
                @click="folderPathChanged('')" v-else>{{name}}/</text>
            <span v-for="(path, index) in fullPath = this.path.split('/').slice(0,-1)" :key="path">
              <text
                  @drop="onDrop($event, '/'+ fullPath.slice(1, index+1)[0])"
                  @dragenter.prevent
                  @dragover.prevent
                  @dragenter="addClass"
                  @dragleave="removeClass"
                  @mouseleave.self="removeClass"
                  class="hover"
                  @click="folderPathChanged('/'+fullPath.slice(1, index+1)[0])"
                  v-if="path != ''">{{ path }}/</text>
            </span>
            <text>
              {{this.path.split('/').slice(-1)[0]}}
            </text>
          </div>
        </ProjectFolderHeader>
    </div>
    <div>
      <div class="row">
        <div class="col-sm-4" v-show="this.path != ''">
          <ProjectFolder
          :name="'Go Back'"
          :shared="'goback'"
          :path="this.previousPath"
          @click="folderPathChanged(this.previousPath)"
          >
          </ProjectFolder>
        </div>
        <div v-for="folder in searched_folders" :key="folder" class="col-sm-4">
          <div v-if="folderNameInSearchTerm(folder)">
            <ProjectFolder
              :directorypath="this.path"
              :projectid="this.$route.params.id"
              :name="folder"
              :path="this.path + '/' + folder"
              :shared="'no'"

              @currentPathChanged="folderPathChanged"
              @folderMoved="setFolders()"
              @folderDeleted="setFolders()"
              @nameChanged="setFolders()"

              @dragenter="addClass"
              @dragleave.self="removeClass"
              @mouseleave.self="removeClass"

              @drop="onDrop($event, this.path + '/' + folder)"
              @dragenter.prevent
              @dragover.prevent
              draggable="true"
              @dragstart="startDrag($event, this.path + '/' + folder)"
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
  props: ["path","name"],
  watch: {
    path(newPath) {
      this.currentPath = newPath;
      this.setFolders();
    },
  },
  data: function () {
    return {
      folders: [],
      searched_folders: [],
      search_term: "",
      currentPath: this.path,
      previousPath: this.path,
      projectid: this.$route.params.id,
      last_target: "",
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
    setSearchTerm(value) {
      this.search_term = value;
      this.setSearchedFolders(value);
    },
    onDrop(event, to) {
      const path = event.dataTransfer.getData('path')
      let id = this.projectid
      if (to === path)
        return
      if (event.dataTransfer.getData('type') === 'file') {
        FilestorageService.moveFile(id, path, to)
            .then(() => {
              this.$emit("fileMoved");
            })
            .catch((err) => {
              AlertService.handleError(err);
            });
      }
      else{
        FilestorageService.moveFolder(id ,path,to, '')
            .then(() => {
              this.setFolders()
            })
            .catch((err) => {
              AlertService.handleError(err);
            });
      }
    },
    folderNameInSearchTerm(folder_name, search_term) {
      return folder_name.includes(search_term) || search_term == null;
    },
    folderPathChanged(path) {
      this.searched_folders = []
      if(Array.isArray(path)){
        this.currentPath = ""
        for(var element in path){
          this.currentPath += "/" + path[element]
        }
        this.$router.push("/project/" + this.projectid + this.currentPath);
        this.$emit("currentPathChanged", this.currentPath);
      }
      else{
        this.currentPath = path;
        this.$router.push("/project/" + this.projectid + path);
        this.$emit("currentPathChanged", this.currentPath);
      }
      this.getPreviousPath();
    },
    setFolders(path=this.path) {
      FilestorageService.getFoldersOfProject(this.projectid, path)
        .then((response) => {
          console.log('Resetting Folders')
          this.folders = response;
          this.setSearchedFolders(this.searchTerm);
        })
        .catch((err) => {
          console.log('resetting Folders Failed')
          AlertService.handleError(err);
        });
    },
    getPreviousPath(){
      this.previousPath = ""
      var pathArray = this.currentPath.split("/")
      pathArray.pop()
      for(var element in pathArray){
        if(pathArray[element] != "") {
          this.previousPath += "/" + pathArray[element]
        }
      }
      console.log(this.previousPath)
    },
    setSearchedFolders(search_term){
      if(search_term == "" || search_term == null){
          this.searched_folders = this.folders  
      }
      else{
        this.searched_folders = []
        for(var folder_index in this.folders){
          if(this.folderNameInSearchTerm(this.folders[folder_index], search_term)){
            this.searched_folders.push(this.folders[folder_index])
          }
        }
      }
    },
  },
  async created() {
    //this.$emit("newHeaderTitle", "NAAM + PAD");
    this.setFolders();
    this.getPreviousPath();
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