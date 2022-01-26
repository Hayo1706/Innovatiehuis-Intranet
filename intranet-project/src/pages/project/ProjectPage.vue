<template>
  <div>
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-8">
          <div class="component-container">
            <div class="component-header">
              <text v-if="this.currentPath == '' && this.parentID == null && this.childID == null">
                Bestandsoverzicht
              </text>
               <text v-else
                  class="hover"
                  @click="currentPathChanged('', this.projectID)">
                Home/                  
              </text>
              <span v-for="(path, index) in this.currentPath.split('/').slice(0,-1)" :key="path">
                <text
                  class="hover"
                  @click="currentPathChanged('/' + this.currentPath.split('/').slice(1, index+1)[0], this.projectID)"
                  v-if="path != ''">{{path}}/
                </text>
              </span>
              <text>
                {{this.currentPath.split('/').slice(-1)[0]}}
              </text>


              <ProjectPageHeader
                :currentPath="this.currentPath"
                @newFolderAdded="currentFoldersChanged()"
                @newFilesUploaded="currentFilesChanged()"
                @deleteSelectedElements="deleteSelectedElements()"
                @searchBarChanged="setSearchTerm">
              </ProjectPageHeader>
            </div>
            <FoldersView
                :previousPath="this.previousPath"
                :currentPath="this.currentPath"
                :projectID="this.projectID"
                :currentFolders="this.currentFolders"
                :searchTerm="this.searchTerm"


                @currentFoldersChanged="currentFoldersChanged"
                @currentFilesChanged="currentFilesChanged"
                @currentPathChanged="currentPathChanged"
                @folderSelected="selectFolder"
                @folderDeselected="deselectFolder"
                @fileMoved="currentFilesChanged"
              />
              <FilesView ref="child" 
              :currentPath="this.currentPath"
              :projectID="this.projectID"
              :currentFolders="this.currentFolders"
              :currentFiles="this.currentFiles"
              :sharedChilds="this.sharedChilds"
              :searchTerm="this.searchTerm"
              
              @sharedFilesChanged="sharedFilesChanged"
              @currentFilesChanged="currentFilesChanged"
              @fileSelected="selectFile"
              @fileDeselected="deselectFile"
              />
              
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
import ProjectPageHeader from "./ProjectPageHeader.vue";
import AnnouncementWindow from "../../shared_components/AnnouncementWindow.vue";
import AlertService from "../../services/AlertService";
import ProjectService from "../../services/ProjectService.js";
import FilestorageService from "../../services/FilestorageService.js";

export default {
  components: { FilesView, FoldersView, AnnouncementWindow, ProjectPageHeader  },
  name: "ProjectPage",
  data: function () {
    return {
      announcementWindowKey: 0,

      projectID: this.getProjectId(),
      projectName: "",
      projectParents: [],
      parentID: this.$route.query.parent,
      childID: this.$route.query.child, 

      searchTerm: "",

      previousPath: this.getPath(),
      currentPath: this.getPath(),
      currentFiles: [],
      currentFolders: [],
      sharedChilds: [],

      selectedFolders: [],
      selectedFiles: [],
    };
  },
  methods: {
    resetSelectedElements(){
      this.selectedFolders = []
      this.selectedFiles = []
    },
    async deleteSelectedFolders(){
      for(var folder of this.selectedFolders){
        FilestorageService.deleteFolder(this.projectID, folder.path, false)
        .then((response) => {
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          if(err.response.status === 409){
            if(confirm("There are elements in " + folder.name + ", are you sure you want to delete it?")){
              FilestorageService.deleteFolder(this.projectID, folder.path, true)
              .then((response) => {
                AlertService.handleSuccess(response);
              })
              .catch((err) => {
                AlertService.handleError(err);
              });
            }
          }
          if (err.response) {
            AlertService.handleError(err);
          }
        });
      }
    },
    async deleteSelectedFiles(){
      for(var file of this.selectedFiles){
        FilestorageService.deleteFile(this.projectID, file.path)
        .then((response) => {
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
      }
    },
    async deleteSelectedElements(){
      await this.deleteSelectedFolders().then(() => {
        this.currentFoldersChanged();
      }).then(()=> {
        this.deleteSelectedFiles().then(() => {
          this.currentFilesChanged();
        }).then(() => {
          this.resetSelectedElements();
        })
      })
      
    },
    selectFolder(folder){
      this.selectedFolders.push(folder)
    },
    deselectFolder(folder){
      for(var folderIndex in this.selectedFolders){
        if(folder.path == this.selectedFolders[folderIndex].path){
          this.selectedFolders.splice(folderIndex, 1)
        }
      }
    },
    selectFile(file){
      this.selectedFiles.push(file)
    },
    deselectFile(file){
      for(var fileIndex in this.selectedFiles){
        if(file.path == this.selectedFiles[fileIndex].path){
          this.selectedFiles.splice(fileIndex, 1)
        }
      }
    },
    currentFoldersChanged(){
      this.setCurrentFolders();
      this.selectedFolders = [];
    },
    currentFilesChanged(){
      this.getChildProjects();
      this.setCurrentFiles();
      this.selectedFiles = [];
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
    setSearchTerm(searchTerm) {
      this.searchTerm = searchTerm;
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
          this.setParentFolders();
          this.setChildFolders();       
        }
      }
      else{
        this.currentFolders.push({'name': 'Ga Terug', 'path': this.previousPath, 'projectID': this.projectID, 'type':'goback'})
      }
      return this.currentFolders
    },
    setChildFolders() {
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
    },
    setParentFolders() {
      ProjectService.getParentsById(this.projectID)
        .then((response) => {
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
    },
    setCurrentFiles() {
      this.currentFiles = []
      if(this.parentID == null && this.childID == null){
        FilestorageService.getFilesOfPath(this.projectID, this.currentPath)
        .then((response) => {
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
          this.setParentFiles();
        }
        else{
          this.setChildFiles();
        }
      }
      return this.currentFiles
    },
    setParentFiles(){
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
    },
    setChildFiles(){
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
    },
    getChildProjects(){
      this.sharedChilds = []
      ProjectService.getChildrenById(this.projectID)
        .then((response) => {
          for(var child of response.data.result){
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