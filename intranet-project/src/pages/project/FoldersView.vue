<template>
    <div>
      <ProjectFolderHeader
      @newFolderAdded="(id) => addFolder(id)"/>
      <div class="container-fluid">
        <div class="row">
          <div v-for="folder in folders" :key="folder" class="col-sm-3">
            <ProjectFolder
              :naam="folder"
              :path="folder"
              :shared='no'
            />
            </div>
        </div>
      </div>
    </div>
</template>

<script>
import ProjectService from "@/services/ProjectService.js";
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
    return { folders: [],
     };
  },
  methods: {
    addFolder(val){ 
      this.folders.push(val);
    },
  },
  async created() {
    //this.$emit("newHeaderTitle", "NAAM + PAD");
    ProjectService.getFoldersOfProject(this.$route.params.id)
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