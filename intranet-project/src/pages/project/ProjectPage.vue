<template>
  <div>
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-8">
          <div class="component-container">
            <FoldersView
                :name="this.name"
                :path="this.path"
                @currentPathChanged="pathChanged"
                @fileMoved="$refs.child.setFiles()"
              />
              <FilesView ref="child" :path="this.path" />
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
import AlertService from "../../services/AlertService";

export default {
  components: { FilesView, FoldersView, AnnouncementWindow },
  name: "ProjectPage",
  data: function () {
    return {
      announcementWindowKey: 0,
      projectId: this.$route.params.id,
      name: "",
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
        this.name = response[0].project_name;
        this.$emit("newHeaderTitle", response[0].project_name);
        AlertService.handleSuccess(response);
      })
      .catch((err) => {
        AlertService.handleError(err);
      });
  },
};
</script>

<style>
</style>