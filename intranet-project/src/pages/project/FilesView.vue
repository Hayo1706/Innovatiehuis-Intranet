<template>
  <div>
    <div class="component-header">
        <ProjectFilesHeader
          :path="this.folderPath"
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
          <div v-if="fileNameInSearchterm(file)">
            <ProjectFile
              :projectid="this.$route.params.id"
              :name="file"
              :type="file.split('.').pop()"
              :path="this.folderPath + '/' + file"
              :directorypath="this.folderPath"
              :shared="'no'"
              @fileDeleted="setFiles()"
              @nameChanged="setFiles()"
              @fileMoved="setFiles()"
              draggable="true"
              @dragstart="startDrag($event, this.folderPath + '/' + file)"
            />
          </div>
        </div>
        <div
            v-for="file in shared_files" :key="file"
            class="col-sm-2"
        >
          <div v-if="fileNameInSearchterm(file.name)">
            <ProjectFile
              :projectid="file['projectid']"
              :name="file['name']"
              :type="file['name'].split('.').pop()"
              :path="file['path']"
              :directorypath="file['path']"
              :shared="'yes'"
            />
          </div>
        </div>
      </div>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import ProjectService from "@/services/ProjectService.js";
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
  props: ['projectID', 'currentPath', 'previousPath', 'currentFolders', 'currentFiles', 'sharedParents'],
  watch: {
    currentPath(newPath) {
      this.folderPath = newPath;
      this.setFiles();
    },
  },
  data: function () {
    return {
      files: [],
      folderPath: this.currentPath,
      shared_files: [],
      projectid: this.$route.params.id,
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
    setFiles() {
      console.log(this.projectID, this.folderPath)
      FilestorageService.getFilesOfPath(this.projectID, this.folderPath)
        .then((response) => {
          this.files = response;
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    getSharedFiles(){
      this.shared_files = []
      ProjectService.getParentsById(this.projectid)
      .then((response) => {
        for(var project_index in response){
          var parentid = response[project_index].projectid
          if(response[project_index].shared_files.length > 0){
            var project_shared_files = response[project_index].shared_files.split(" ")
            for(var file_index in project_shared_files){
              let file_path = "/" + project_shared_files[file_index]
              let file_path_array = file_path.split("/")
              let file_name = file_path_array[file_path_array.length-1]
              console.log(response[project_index].project_name)
              this.shared_files.push({"projectid": parentid, "path": file_path, "name": file_name})
            }
          }
        }
      })
      .catch((err) => {
        console.log(err)
          if (err.response) {
            console.log(err.response.status);
          }
      })
    }
  },
  async created() {
    this.setFiles();
    this.getSharedFiles();

  },
};
</script>

<style scoped>
.component-container{
  height: auto;
  min-height: auto;
}
</style>