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
                @fileMoved="currentFilesChanged"
              />
              <FilesView ref="child" 
              :currentPath="this.currentPath"
              :projectID="this.projectID"
              :currentFolders="this.currentFolders"
              :currentFiles="this.currentFiles"
              
              @sharedFilesChanged="sharedFilesChanged"
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
      childID: this.$route.query.child, 

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
    sharedFilesChanged(sharedFiles){
      const project = {
        shared_files: sharedFiles
      }
      ProjectService.updateSharedFilesOfProject(this.projectID, this.childID, project)
      .then((response) => {
        this.setCurrentFiles();
        AlertService.handleSuccess(response);
      })
      .catch((err) => {
        AlertService.handleError(err);
      })
    },
    currentPathChanged(path, familyID) {
      this.projectID = this.getProjectId();
      this.previousPath = this.currentPath;
      this.$router.push("/project/" + this.projectID + path)

      if(this.projectID == familyID){
        this.parentID = null;
        this.childID = null;
        this.currentPath = path
      }
      else{
        this.currentPath = ""
        if(path.includes("child")){
          this.childID = familyID
        }
        else if(path.includes("parent")){
          this.parentID = familyID
        }
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
      if(this.parentID == null && this.childID == null){

        FilestorageService.getFoldersOfProject(this.projectID, this.currentPath)
          .then((response) => {
            for(var folder in response){
              this.currentFolders.push({'name': response[folder], 'path': this.currentPath + '/' + response[folder], 'projectID': this.projectID, 'type':'normal'})
            }
          })
          .catch((err) => {
            AlertService.handleError(err);
        });
        if(this.currentPath == ''){
          ProjectService.getParentsById(this.projectID)
            .then((response) => {
              for(var parent in response){
                var parentID = response[parent].projectid
                var parentName = response[parent].project_name
                this.currentFolders.push({'name': parentName, 'path': '/', 'projectID': parentID, 'type':'shared'})         
              }
            })
            .catch((err) => {
              AlertService.handleError(err);
            })
          
          ProjectService.getChildrenById(this.projectID)
          .then((response) => {
            for(var child in response){
              var childName = response[child].project_name
              var childID = response[child].projectid
              this.currentFolders.push({'name': childName, 'path': '/', 'projectID': childID, 'type':'owned'})
            }
          })
          .catch((err) => {
            AlertService.handleError(err)
          })
          
        }
      }
      else{
        this.currentFolders.push({'name': 'Go Back', 'path': this.previousPath, 'projectID': this.projectID, 'type':'goback'})
      }
      return this.currentFolders

    },
    setCurrentFiles() {
      this.currentFiles = []
      if(this.parentID == null && this.childID == null){
        FilestorageService.getFilesOfPath(this.projectID, this.currentPath)
        .then((response) => {
          for(var file in response){
            this.currentFiles.push({'name': response[file], 'path': this.currentPath + '/' + response[file], 'projectID': this.projectID, 'type':'normal'})
          }
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
      }
      else{
        if(this.parentID != null){
          ProjectService.getParentsById(this.projectID)
          .then((response) => {

            for(var parent in response){
              var parentID = response[parent].projectid
              if(this.parentID == parentID){
                var sharedFiles = response[parent].shared_files.split(" ")
                for(var file in sharedFiles){
                  var fileName = sharedFiles[file].split("/").pop()
                  this.currentFiles.push({'name': fileName, 'path': sharedFiles[file], 'projectID': parentID, 'type':'shared'})
                }
              }              
            }
          })
          .catch((err) => {
            AlertService.handleError(err);
          })
        }
        else{
          ProjectService.getChildrenById(this.projectID)
          .then((response) => {
            for(var child of response){
              var childID = child.projectid
              if(childID == this.childID){
                var sharedFiles = child.shared_files.split(" ")
                for(var file of sharedFiles){
                  var fileName = file.split("/").pop()
                  this.currentFiles.push({'name': fileName, 'path': file, 'projectID': this.projectID, 'type':'owned'})
                }
              }
            }
          })
          .catch((err) => {
            AlertService.handleError(err)
          })
        }
      }
      return this.currentFiles
    },
    setProjectName() {
      ProjectService.getProjectById(this.$route.params.id)
      .then((response) => {
        this.projectName = response[0].project_name;
        this.$emit("newHeaderTitle", response[0].project_name);
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