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
                :path="'/' + folder"
                :shared='no'
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
  props: [
  ],
  data: function () {
    return { 
      folders: [],
      searchTerm: "",
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
  },
  async created() {
    //this.$emit("newHeaderTitle", "NAAM + PAD");
    FilestorageService.getFoldersOfProject(this.$route.params.id)
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
}
</script>


<style scoped>
.row{
  font-size: calc(0.7vw + 0.7vh);
  text-align: left;
}
</style>