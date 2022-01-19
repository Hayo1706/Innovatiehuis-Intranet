<template>
  <div>
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-8">
          <div class="component-container">
            <FoldersView
                :previousPath="this.previousPath"
                :currentPath="this.currentPath"
                :projectID="this.projectID"
                :currentFolders="this.currentFolders"
                :sharedParents="this.sharedParents"

                @currentFoldersChanged="currentFoldersChanged"
                @currentPathChanged="currentPathChanged"
                @fileMoved="$refs.child.setFiles()"
              />
              <FilesView ref="child" 
              :currentPath="this.currentPath"
              :projectID="this.projectID"
              :currentFolders="this.currentFolders"
              :currentFiles="this.currentFiles"/>
          </div>
        </div>
        <div class="col-sm-4">
            <AnnouncementWindow
              @reload="reloadAnnouncementWindow()"
              :key="this.announcementWindowKey"
              >Mededelingen</AnnouncementWindow
            >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilesView from "./FilesView.vue";
import FoldersView from "./FoldersView.vue";
import AnnouncementWindow from "../../shared_components/AnnouncementWindow.vue";
import ProjectService from "../../services/ProjectService.js";
import FilestorageService from "../../services/FilestorageService.js";

export default {
  components: { FilesView, FoldersView, AnnouncementWindow },
  name: "ProjectPage",
  data: function () {
    return {
      announcementWindowKey: 0,

      projectID: this.getProjectId(),
      projectName: "",
      projectParents: [],
      parentID: this.$route.query.parentID,

      previousPath: this.getPath(),
      currentPath: this.getPath(),
      currentFiles: [],
      currentFolders: this.setCurrentFolders(),
      sharedParents: [],
    };
  },
  methods: {
    currentFoldersChanged(){
      this.setCurrentFolders();
    },
    currentPathChanged(path) {
      this.projectID = this.getProjectId();
      this.previousPath = this.currentPath;
      this.currentPath = path;
      this.$router.push("/project/" + this.projectID + this.currentPath)
      this.setCurrentFolders();
    },
    reloadAnnouncementWindow() {
      this.announcementWindowKey += 1;
    },
    getPath(){
      let childid = this.$route.query.child;
      if(childid != null){
        return "/"
      }
      return this.$route.fullPath.split("/project/")[1].split(this.$route.params.id)[1]
    },
    getProjectId(){
      if(this.$route.query.parent != null){
        return this.$route.query.parent
      }
      return this.$route.params.id
    },
    setCurrentFolders() {
      FilestorageService.getFoldersOfProject(this.projectID, this.currentPath)
        .then((response) => {
          this.currentFolders = []
          for(var folder in response){
            this.currentFolders.push({'name': response[folder], 'path': this.currentPath + '/' + response[folder], 'projectID': this.projectID, 'type':'normal'})
          }
          return this.currentFolders
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
          return []
        });
    },
    setCurrentFiles() {
      FilestorageService.getFilesOfPath(this.projectID, this.currentPath)
      .then((response) => {
        this.currentFiles = []
        for(var file in response){
          this.currentFiles.push({'name': response[file], 'path': this.currentPath + '/' + response[file], 'projectID': this.projectID, 'type':'normal'})
        }
        console.log(this.currentFiles)
        return this.currentFiles
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        return []
      });
    },
    setProjectName() {
      ProjectService.getProjectById(this.$route.params.id)
      .then((response) => {
        this.projectName = response[0].project_name;
        this.$emit("newHeaderTitle", response[0].project_name);
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
          this.$emit("newHeaderTitle", "Project #" + this.$route.params.id);
        }
      });
    }
  },
  
  async created() {
    this.setProjectName();
    this.setCurrentFolders();
    this.setCurrentFiles();

  },
};
</script>

<style>
</style>