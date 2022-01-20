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
          for(var file in response){
            this.currentFiles.push({'name': response[file], 'path': this.currentPath + '/' + response[file], 'projectID': this.projectID, 'type':'normal'})
          }
          return this.currentFiles
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
          return []
        });
      }
      else{
        ProjectService.getParentsById(this.projectID)
          .then((response) => {
            this.currentFiles = []
            for(var parent in response){
              var parentID = response[parent].projectid
              var sharedFiles = response[parent].shared_files.split(" ")
              if(this.parentID == parentID){
                for(var file in sharedFiles){
                  var fileName = sharedFiles[file].split("/").pop()
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
      }
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