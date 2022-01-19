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
              :sharedParents="this.sharedParents"
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
      if(this.$route.query.child != null){
        return this.$route.query.child
      }
      return this.$route.params.id
    },
    setCurrentFolders() {
      FilestorageService.getFoldersOfProject(this.projectID, this.currentPath)
        .then((response) => {
          this.currentFolders = response

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
        this.currentFiles = response;
        return response;
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        return []
      });
    },
    setSharedParents(){
      this.sharedParents = []
      ProjectService.getParentsById(this.projectID)
      .then((response) => {
        this.sharedParents = response
      })
      .catch((err) => {
        console.log(err)
          if (err.response) {
            console.log(err.response.status);
          }
      })
    },
    setParentProjects() {
      this.projectParents = []
      ProjectService.getParentsById(this.projectID)
      .then((response) => {
        for(var index in response){
          var parentID = response[index].projectID
          var parentName = response[index].project_name
          this.projectParents.push({"projectID": parentID, "projectName": parentName})
        }
      })
      .catch((err) => {
        console.log(err)
          if (err.response) {
            console.log(err.response.status);
          }
      })
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
    this.setSharedParents();
    this.setCurrentFiles();

  },
};
</script>

<style>
</style>