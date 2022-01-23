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

                @currentFoldersChanged="currentFoldersChanged"
                @currentFilesChanged="currentFilesChanged"
                @currentPathChanged="currentPathChanged"
                @fileMoved="$refs.child.setFiles()"
              />
              <FilesView ref="child" 
              :currentPath="this.currentPath"
              :projectID="this.projectID"
              :currentFolders="this.currentFolders"
              :currentFiles="this.currentFiles"
              
              @currentFilesChanged="currentFilesChanged"/>
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
import AlertService from "../../services/AlertService";
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
      parentID: this.$route.query.parent,

      previousPath: this.getPath(),
      currentPath: this.getPath(),
      currentFiles: [],
      currentFolders: [],
      sharedParents: [],
    };
  },
  methods: {
    currentFoldersChanged(){
      this.setCurrentFolders();
    },
    currentFilesChanged(){
      this.setCurrentFiles();
    },
    currentPathChanged(path, parentID) {
      this.projectID = this.getProjectId();
      this.previousPath = this.currentPath;
      this.$router.push("/project/" + this.projectID + path)

      if(this.projectID == parentID){
        this.parentID = null;
        this.currentPath = path
      }
      else{
        this.parentID = parentID
      }
      this.setCurrentFolders();
      this.setCurrentFiles();
     
    },
    reloadAnnouncementWindow() {
      this.announcementWindowKey += 1;
    },
    getPath(){
      return this.$route.path.split("/project/")[1].split(this.$route.params.id)[1]
    },
    getProjectId(){
      return this.$route.params.id
    },
    setCurrentFolders() {
      this.currentFolders = []
      if(this.parentID == null){

        FilestorageService.getFoldersOfProject(this.projectID, this.currentPath)
          .then((response) => {
            for(var folder in response.data.result){
              this.currentFolders.push({'name': response.data.result[folder], 'path': this.currentPath + '/' + response.data.result[folder], 'projectID': this.projectID, 'type':'normal'})
            }
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            AlertService.handleError(err);
        });
        if(this.currentPath == ''){
          ProjectService.getParentsById(this.projectID)
            .then((response) => {
              for(var parent in response.data.result){
                var parentID = response.data.result[parent].projectid
                var parentName = response.data.result[parent].project_name
                var sharedFiles = response.data.result[parent].shared_files.split(" ")
                this.currentFolders.push({'name': parentName, 'path': '/', 'projectID': parentID, 'type':'shared', 'files': sharedFiles})         
              }
              AlertService.handleSuccess(response);
            })
            .catch((err) => {
              AlertService.handleError(err);
            })
        }
      }
      else{
        this.currentFolders.push({'name': 'Go Back', 'path': this.previousPath, 'projectID': this.projectID, 'type':'goback'})
      }
      return this.currentFolders

    },
    setCurrentFiles() {
      if(this.parentID == null){
        FilestorageService.getFilesOfPath(this.projectID, this.currentPath)
        .then((response) => {
          this.currentFiles = []
          for(var file in response.data.result){
            this.currentFiles.push({'name': response.data.result[file], 'path': this.currentPath + '/' + response.data.result[file], 'projectID': this.projectID, 'type':'normal'})
          }
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
      }
      else{
        ProjectService.getParentsById(this.projectID)
          .then((response) => {
            this.currentFiles = []
            for(var parent in response.data.result){
              var parentID = response.data.result[parent].projectid
              var sharedFiles = response.data.result[parent].shared_files.split(" ")
              if(this.parentID == parentID){
                for(var file in sharedFiles){
                  var fileName = sharedFiles[file].split("/").pop()
                  this.currentFiles.push({'name': fileName, 'path': "/" + sharedFiles[file], 'projectID': parentID, 'type':'shared'})
                }
              }              
            }
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            AlertService.handleError(err);
          })
      }
    },
    setProjectName() {
      ProjectService.getProjectById(this.$route.params.id)
      .then((response) => {
        this.projectName = response.data.result[0].project_name;
        this.$emit("newHeaderTitle", response.data.result[0].project_name);
        AlertService.handleSuccess(response);
      })
      .catch((err) => {
        AlertService.handleError(err);
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