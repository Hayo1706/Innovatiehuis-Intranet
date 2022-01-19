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
    currentPathChanged(path) {
      this.projectID = this.getProjectId();
      this.previousPath = this.currentPath;
      this.$router.push("/project/" + this.projectID + path)

      if(path.startsWith("?")){
        var typeID = path.split("?")[1].split("=")[0]
        var ID = path.split("?")[1].split("=")[1]
        if(typeID == "parent"){
          alert("GAY")
          this.setCurrentSharedFiles(ID)
          alert(this.currentFiles);
        }
      }
      
      else{
        this.currentPath = path
      }
      this.setCurrentFolders();
      this.setCurrentFiles();

    },
    reloadAnnouncementWindow() {
      this.announcementWindowKey += 1;
    },
    getPath(){
      let parent = this.$route.query.parent;
      if(parent != null){
        return this.$route.params.id
      }
      return this.$route.fullPath.split("/project/")[1].split(this.$route.params.id)[1]
    },
    getProjectId(){
      return this.$route.params.id
    },
    setCurrentFolders() {
      this.currentFolders = []
      FilestorageService.getFoldersOfProject(this.projectID, this.currentPath)
        .then((response) => {
          for(var folder in response){
            this.currentFolders.push({'name': response[folder], 'path': this.currentPath + '/' + response[folder], 'projectID': this.projectID, 'type':'normal'})
          }
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
      });
      if(this.currentPath == ''){
        ProjectService.getParentsById(this.projectID)
          .then((response) => {
            for(var parent in response){
              var parentID = response[parent].projectid
              var parentName = response[parent].project_name
              var sharedFiles = response[parent].shared_files.split(" ")
              this.currentFolders.push({'name': parentName, 'path': '/', 'projectID': parentID, 'type':'shared', 'files': sharedFiles})
              
            }
          })
          .catch((err) => {
            console.log(err)
              if (err.response) {
                console.log(err.response.status);
              }
          })
      }
      return this.currentFolders

    },
    setCurrentSharedFiles(requestedID) {
      ProjectService.getParentsById(this.projectID)
          .then((response) => {
            this.currentFiles = []
            for(var parent in response){
              var parentID = response[parent].projectid
              var sharedFiles = response[parent].shared_files.split(" ")
              if(parentID == requestedID){
                for(var file in sharedFiles){
                  var fileName = sharedFiles[file].split("/").pop()
                  alert(parentID)
                  this.currentFiles.push({'name': fileName, 'path': "/" + sharedFiles[file], 'projectID': parentID, 'type':'shared'})
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