<template>
  <div>
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-8">
            <div class="row">
              <div class="col-sm">
                <FoldersView 
                :path ="this.path"
                @currentPathChanged="pathChanged"
               />
              </div>
            </div>
            <div class="row">
              <div class="col-sm">
                <FilesView 
                :path ="this.path"/>
              </div>
            </div>
        </div>
        <div class="col-sm-4">
            <div class="row">
              <AnnouncementWindow @reload="reloadAnnouncementWindow()" :key="this.announcementWindowKey">Mededelingen</AnnouncementWindow>
            </div>
            <div class="row">
                <ChatWindow></ChatWindow>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilesView from './FilesView.vue';
import FoldersView from './FoldersView.vue';
import ChatWindow from './ChatWindow.vue';
import AnnouncementWindow from '../../shared_components/AnnouncementWindow.vue';
import ProjectService from "../../services/ProjectService.js";


export default {
  components: { FilesView, FoldersView, AnnouncementWindow, ChatWindow },
  name: "ProjectPage",
  data: function () {
    return {
      announcementWindowKey: 0,
      projectId: this.$route.params.id,
      path: this.$route.fullPath.split("/project/")[1].split(this.$route.params.id)[1]
    };
  },
  methods: {
    pathChanged(path){
      this.path = path
    },
    reloadAnnouncementWindow() {
      this.announcementWindowKey += 1;
    },
  },
  async created() {
    ProjectService.getProjectById(this.$route.params.id)
      .then((response) => {
        this.$emit('newHeaderTitle', 'Project: ' + response[0].project_name)
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
          this.$emit('newHeaderTitle', 'Project: #' + this.$route.params.id)
        }
        alert(err);
      });
  },
};
</script>

<style>

</style>