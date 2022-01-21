<template>
  <div class="component-container">
    <div class="component-header">
      <slot></slot>
    </div>
    <div id="projects-window" class="component-body">
      <ProjectButton
        v-for="project of projects"
        :key="project.id"
        v-bind:projectId="project.projectid"
        v-bind:projectName="project.project_name"
        v-bind:lastUpdated="project.last_updated"
        v-on:reload="reload()"
      />
    </div>
  </div>
</template>

<script>
import ProjectButton from "./ProjectButton.vue";
import ProjectService from "@/services/ProjectService.js";
import PermissionService from "@/services/PermissionService";
import AlertService from "../services/AlertService";

export default {
  components: { ProjectButton },
  name: "ProjectsWindow",
  props: [],
  data: function () {
    return {
      projects: [],
    };
  },
  async created() {
    ProjectService.getProjectsByUser(localStorage.getItem("userid"))
      .then((response) => {
        this.projects = response.data;
        AlertService.handleSuccess(response);
      })
      .catch((err) => {
        AlertService.handleError(err);
      });
  },
  methods: {
    canReadAllProjects() {
      return PermissionService.userHasPermission("may_read_any_project");
    },
    canReadAllUsers() {
      return PermissionService.userHasPermission("may_read_any_user");
    },
    toProjectsPage() {
      this.$router.push("/manage/projects");
    },
    toUsersPage() {
      this.$router.push("/manage/users");
    },
  },
};
</script>

<style scoped>
</style>