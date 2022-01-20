<template>
  <div>
    <div class="component-header">
        <ProjectFilesHeader
          :path="this.folderPath"
          @searchBarChanged="setSearchTerm"
          @newFilesUploaded="currentFilesChanged"
        >
        Bestanden
        </ProjectFilesHeader>
    </div>
      <div class="row">
        <div v-for="file in files" :key="file" class="col-sm-2">
          <div v-if="fileNameInSearchterm(file.name)">
            <ProjectFile
              :projectID="file.projectID"
              :name="file.name"
              :fileType="file.name.split('.').pop()"
              :path="file.path"
              :type="file.type"
              :currentFolders="this.currentFolders"

              @fileDeleted="currentFilesChanged"
              @nameChanged="currentFilesChanged"
              @fileMoved="currentFilesChanged"
              draggable="true"
              @dragstart="startDrag($event, file.path)"
            />
          </div>
        </div>
      </div>
  </div>
</template>

<script>
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
  props: ['projectID', 'currentPath', 'currentFolders', 'currentFiles'],
  watch: {
    currentPath: function(newPath){
      this.folderPath = newPath;
    },
    currentFiles(newFiles){
      this.files = newFiles;
    },
    currentFolders(newFolders){
      this.folders = newFolders;
    }
  },
  data: function () {
    return {
      files: [],
      folders: [],
      folderPath: this.currentPath,
      searchTerm: "",
    };
  },
  methods: {
    fileNameInSearchterm(name) {
      return name.includes(this.searchTerm) || this.searchTerm == null;
    },
    setSearchTerm(value) {
      this.searchTerm = value;
    },
    currentFilesChanged(){
      this.$emit("currentFilesChanged")
    }
  }
};
</script>

<style scoped>
.component-container{
  height: auto;
  min-height: auto;
}
</style>