<template>
  <div>
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-8">
              <FoldersView
                :path="this.path"
                @currentPathChanged="pathChanged"
              />
              <FilesView :path="this.path" />
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

export default {
  components: { FilesView, FoldersView, AnnouncementWindow },
  name: "ProjectPage",
  data: function () {
    return {
      announcementWindowKey: 0,
      projectId: this.$route.params.id,
      path: this.$route.fullPath
        .split("/project/")[1]
        .split(this.$route.params.id)[1],
    };
  },
  methods: {
    pathChanged(path) {
      this.path = path;
    },
    reloadAnnouncementWindow() {
      this.announcementWindowKey += 1;
    },
  },
  async created() {
    ProjectService.getProjectById(this.$route.params.id)
      .then((response) => {
        this.$emit("newHeaderTitle", "Project: " + response[0].project_name);
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
          this.$emit("newHeaderTitle", "Project: #" + this.$route.params.id);
        }
      });
  },
};
</script>

<style>
</style>