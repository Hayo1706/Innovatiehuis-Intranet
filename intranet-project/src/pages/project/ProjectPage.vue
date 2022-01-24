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
              :sharedChilds="this.sharedChilds"
              
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
      sharedChilds: [],
    };
  },
  methods: {
    currentFoldersChanged(){
      this.setCurrentFolders();
    },
    currentFilesChanged(){
      this.getChildProjects();
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
      this.setCurrentFiles();
      this.setCurrentFolders();     
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
            for(var folder in response.data){
              this.currentFolders.push({'name': response.data[folder], 'path': this.currentPath + '/' + response.data[folder], 'projectID': this.projectID, 'type':'normal'})
            }
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            AlertService.handleError(err);
        });
        if(this.currentPath == ''){
          ProjectService.getParentsById(this.projectID)
            .then((response) => {
              console.log('test1', response)
              for(var parent in response.data.result){
                var parentID = response.data.result[parent].projectid
                var parentName = response.data.result[parent].project_name
                this.currentFolders.push({'name': "Gedeeld door:\n" + parentName, 'path': '/', 'projectID': parentID, 'type':'shared'})         
              }
              AlertService.handleSuccess(response);
            })
            .catch((err) => {
              AlertService.handleError(err);
            })
          
          ProjectService.getChildrenById(this.projectID)
          .then((response) => {
            for(var child in response.data.result){
              var childName = response.data.result[child].project_name
              var childID = response.data.result[child].projectid
              this.currentFolders.push({'name': "Gedeeld met:\n" +childName, 'path': '/', 'projectID': childID, 'type':'owned'})
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
          console.log('test', response.data);
          this.currentFiles = []
          for(var file in response.data){
            this.currentFiles.push({'name': response.data[file], 'path': this.currentPath + '/' + response.data[file], 'projectID': this.projectID, 'type':'normal'})
          }
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
      }
      else{
        if(this.parentID != null){
          ProjectService.getParentsById(this.projectID)
          .then((response) => {

            for(var parent of response.data.result){
              var parentID = parent.projectid
              if(this.parentID == parentID){
                var sharedFiles = parent.shared_files.split(" ")
                for(var file in sharedFiles){
                  var fileName = sharedFiles[file].split("/").pop()
                  this.currentFiles.push({'name': fileName, 'path': sharedFiles[file], 'projectID': parentID, 'type':'shared'})
                }
              }              
            }
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            AlertService.handleError(err);
          })
        }
        else{
          ProjectService.getChildrenById(this.projectID)
          .then((response) => {
            for(var child of response.data.result){
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
        this.projectName = response.data[0].project_name;
        this.$emit("newHeaderTitle", response.data[0].project_name);
        AlertService.handleSuccess(response);
      })
      .catch((err) => {
        AlertService.handleError(err);
      });
    },
    getChildProjects(){
      this.sharedChilds = []
      ProjectService.getChildrenById(this.projectID)
        .then((response) => {
          for(var child of response){
            this.sharedChilds.push(child)
          }
        })
        .catch((err) => {
          AlertService.handleError(err)
        })
    }
  },
  async created() {
    this.setProjectName();
    this.setCurrentFolders();
    this.setCurrentFiles();
    this.getChildProjects();
  },
};
</script>

<style>
</style>