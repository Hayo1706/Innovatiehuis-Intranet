<template>
  <div>
    <ProjectFolderHeader
      :path="this.currentPath"
      @newFolderAdded="(id) => reloadFolders()"
      @searchBarChanged="setSearchTerm"
    />
    <div class="container-fluid">
      <div class="row">
        <div v-for="folder in folders" :key="folder" class="col-sm-3">
          <div v-if="folderNameInSearchTerm(folder)">
            <ProjectFolder
              :directorypath="this.path"
              :projectid="this.$route.params.id"
              :name="folder"
              :path="this.path + '/' + folder"
              :shared="no"
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
      searchTerm: "",
      currentPath: this.path,
      projectid: this.$route.params.id,
    };
  },
  methods: {
    reloadFolders() {
      location.reload();
    },
    setSearchTerm(value) {
      this.searchTerm = value;
    },
    folderNameInSearchTerm(name) {
      if (name.includes(this.searchTerm) || this.searchTerm == null) {
        return true;
      } else {
        return false;
      }
    },
    folderPathChange(path) {
      this.currentPath = path;
      this.$router.push("/project/" + this.projectid + path);
      this.$emit("currentPathChanged", this.currentPath);
    },
    setFolders() {
      FilestorageService.getFoldersOfProject(this.projectid, this.path)
        .then((response) => {
          this.folders = response;
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
  },
  async created() {
    //this.$emit("newHeaderTitle", "NAAM + PAD");
    this.setFolders();
  },
};
</script>


<style scoped>
.row {
  font-size: calc(0.7vw + 0.7vh);
  text-align: left;
}
</style>