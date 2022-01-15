<template>
    <div class="component-header">
        <ProjectFilesHeader
          :path="this.path"
          @searchBarChanged="setSearchTerm"
          @newFilesUploaded="setFiles()"
        >
        <text>Bestanden</text>
        </ProjectFilesHeader>
    </div>
      <div class="row">
        <div
            v-for="file in files" :key="file"
            class="col-sm-2"

        >
          <!--- Determine size of each Column --->
          <div v-if="fileNameInSearchterm(file)">
            <!--- Ensures that height is equal to width --->
            <ProjectFile
              :projectid="this.$route.params.id"
              :name="file"
              :type="file.split('.').pop()"
              :path="this.path + '/' + file"
              :directorypath="this.path"
              :shared="'no'"
              @fileDeleted="setFiles()"
              @nameChanged="setFiles()"
              @fileMoved="setFiles()"
              draggable="true"
              @dragstart="startDrag($event, this.path + '/' + file)"
            />
          </div>
        </div>
      </div>

</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import ProjectFilesHeader from "./ProjectFilesHeader.vue";
import ProjectFile from "./ProjectFile.vue";
export default {
  setup(){
    const startDrag = (event, path) => {
      event.dataTransfer.dropEffect = 'move'
      event.dataTransfer.effectAllowed = 'move'
      event.dataTransfer.setData('path', path)
      event.dataTransfer.setData('type', 'file')
    }

    return{
      startDrag,
    }
  },
  components: {
    ProjectFilesHeader,
    ProjectFile,
  },
  name: "FilesView",
  props: ["path"],
  watch: {
    path(newPath) {
      this.currentPath = newPath;
      this.setFiles();
    },
  },
  data: function () {
    return {
      files: [],
      projectid: this.$route.params.id,
      searchTerm: "",
      currentPath: this.path,
    };
  },
  methods: {
    fileNameInSearchterm(name) {
      return name.includes(this.searchTerm) || this.searchTerm == null;
    },
    setSearchTerm(value) {
      this.searchTerm = value;
    },
    setPath(path) {
      this.currentPath = path;
    },
    setFiles() {
      FilestorageService.getFilesOfPath(this.projectid, this.path)
        .then((response) => {
          this.files = response;
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
  },
  async created() {
    this.setFiles();
  },
};
</script>

<style scoped>
.component-container{
  height: auto;
  min-height: auto;
}
</style>