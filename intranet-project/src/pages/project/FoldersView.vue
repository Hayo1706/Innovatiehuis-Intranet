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
              :shared="no"
              @currentPathChanged="folderPathChanged"
              @folderMoved="setFolders()"
              @folderDeleted="setFolders()"
              @nameChanged="setFolders()"
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
    folderNameInSearchTerm(folder_name, search_term) {
      if (folder_name.includes(search_term) || search_term == null) {
        return true;
      } else {
        return false;
      }
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
    setFolders() {
      FilestorageService.getFoldersOfProject(this.projectid, this.path)
        .then((response) => {
          this.folders = response;
          this.setSearchedFolders(this.searchTerm);
        })
        .catch((err) => {
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