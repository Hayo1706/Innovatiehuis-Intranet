<template>
  <div class="container-fluid">
    <ProjectInfo
      @nameOrDescriptionChanged="
        (project_obb) => {
          this.$emit(
            'newHeaderTitle',
            project_obb.project_name + ': Instellingen'
          );
        }
      "
      v-bind:project="project"
      v-bind:open="true"
    ></ProjectInfo>
  </div>
</template>

<script>
import ProjectInfo from "@/shared_components/ProjectInfo.vue";
import ProjectService from "@/services/ProjectService.js";
import AlertService from "../../../services/AlertService";

export default {
  components: { ProjectInfo },
  name: "ProjectSettings",
  data: function () {
    return {
      project: {},
    };
  },
  created() {
    ProjectService.getProjectById(this.$route.params.id)
      .then((response) => {
        this.$emit(
          "newHeaderTitle",
          response.data.result[0].project_name + ": Instellingen"
        );
        this.project = response.data.result[0];
        AlertService.handleSuccess(response);
      })
      .catch((err) => {
        AlertService.handleError(err);
      });
  },
};
</script>

<style scoped>
div {
  padding-bottom: 5vh;
}
</style>>
