<template>
    <div>
      <ProjectFolderHeader
        @newFolderAdded="(id) => reloadFolders()"
        @searchBarChanged="setSearchTerm"
      />
      <div class="container-fluid">
        <div class="row">
          <div v-for="folder in folders" :key="folder" class="col-sm-3">
            <div v-if="folderNameInSearchTerm(folder)">
              <ProjectFolder
                :projectid="this.$route.params.id"
                :name="folder"
                :path="this.path + '/' + folder"
                :shared='no'
                @currentPathChanged="folderPathChange"
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
  props: {
    path: { type: String, required: true },
  },
  data: function () {
    return { 
      folders: [],
      searchTerm: "",
      currentPath: this.path
     };
  },
  methods: {
    reloadFolders(){
      location.reload();
    },
    setSearchTerm(value) {
      this.searchTerm = value;
    },
    folderNameInSearchTerm(name){
      if(name.includes(this.searchTerm) || this.searchTerm == null){
        return true;
      }
      else{
        return false;
      }
    },
    folderPathChange(path){
      this.currentPath = path.split("/project/")[1];
      this.setFolders();
      this.$router.push(path);
      this.$emit("currentPathChanged", this.path);
    },
    setFolders(){
      FilestorageService.getFoldersOfProject(this.$route.params.id, this.currentPath)
      .then((response) => {
        this.folders = response;
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });
    },
  },
  async created() {
    //this.$emit("newHeaderTitle", "NAAM + PAD");
    this.setFolders();
  }
}
</script>


<style scoped>
.row{
  font-size: calc(0.7vw + 0.7vh);
  text-align: left;
}
</style>