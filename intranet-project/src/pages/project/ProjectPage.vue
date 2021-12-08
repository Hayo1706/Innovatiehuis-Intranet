<template>
  <div>
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm">
          <div class="container-fluid">
            <div class="row">
              <div class="col-sm">
                <FoldersView />
              </div>
            </div>
            <div class="row">
              <div class="col-sm">
                <FilesView />
              </div>
            </div>
          </div>
        </div>
        <div class="col-sm">
          <AnnouncementWindow @reload="reloadAnnouncementWindow()" :key="this.announcementWindowKey">Mededelingen</AnnouncementWindow>/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilesView from './FilesView.vue';
import FoldersView from './FoldersView.vue';
import AnnouncementWindow from '../../shared_components/AnnouncementWindow.vue';
import ProjectService from "../../services/ProjectService.js";

export default {
  components: { FilesView, FoldersView, AnnouncementWindow },
  name: "ProjectPage",
  data: function () {
    return {
      announcementWindowKey: 0,
      projectId: this.$route.params.id,
      projectName: this.$route.params.id,
    };
  },
  methods: {
      reloadAnnouncementWindow() {
        this.announcementWindowKey += 1;
    }
  },
  async created() {
    ProjectService.getProjectById(this.$route.params.id)
      .then((response) => {
        this.$emit('newHeaderTitle', 'Project: ' + response[0].name)
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