<template>
  <div class="component-container">
    <div class="component-header">
      <ProjectFolderHeader
          :path="this.currentPath"
          @newFolderAdded="(id) => setFolders()"
          @searchBarChanged="setSearchTerm">
          &nbsp;
          <text v-if="this.path == ''">Mappen</text>
          <text @click="folderPathChanged('')" v-else>.../</text>
          <span v-for="(path, index) in fullPath = this.path.split('/')" :key="path">
            <text @click="folderPathChanged(fullPath.slice(1, index+1))" v-if="path != ''">{{ path }}/</text>
          </span>
        </ProjectFolderHeader>
    </div>
    <div>
      <div class="row">
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
  props: ["path"],
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
      projectid: this.$route.params.id,
    };
  },
  methods: {
    setSearchTerm(value) {
      this.search_term = value;
      this.setSearchedFolders(value);
    },
    onDrop(event, to) {
      const path = event.dataTransfer.getData('path')
      let id = this.projectid
      if (event.dataTransfer.getData('type') === 'file') {
        FilestorageService.moveFile(id, path, to)
            .then(() => {
              console.log("1.Moving File...")
              this.$emit("fileMoved");
            })
            .catch((err) => {
              if (err.response) {
                console.log(err.response.status);
              }
            });
      }
      else{
        FilestorageService.moveFolder(id ,path,to, '')
            .then(() => {
              console.log('1.Moving Folder')
              console.log(2)
              this.setFolders()
            })
            .catch((err) => {
              if (err.response) {
                console.log(err.response.status);
              }
            });
      }
    },
    folderNameInSearchTerm(folder_name, search_term) {
      return folder_name.includes(search_term) || search_term == null;
    },
    folderPathChanged(path) {
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
      
    },
    setFolders(path=this.path) {
      console.log(path)
      FilestorageService.getFoldersOfProject(this.projectid, path)
        .then((response) => {
          console.log('Resetting Folders')
          this.folders = response;
          this.setSearchedFolders(this.searchTerm);
        })
        .catch((err) => {
          console.log('resetting Folders Failed')
          if (err.response) {
            console.log(err.response.status);
          }
        });
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
    }
  },
  async created() {
    //this.$emit("newHeaderTitle", "NAAM + PAD");
    this.setFolders();
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