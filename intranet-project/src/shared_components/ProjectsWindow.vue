<template>
  <div class="component-container">
    <div class="component-header">
      <slot></slot>
    </div>
    <div
      class="full-button"
      v-show="canReadAllProjects()"
      @click="toProjectsPage()"
    >
      Alle Projecten
    </div>
    <div class="full-button" v-show="canReadAllUsers()" @click="toUsersPage()">
      Alle Gebruikers
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
        this.projects = response;
        console.log("API RESPONDS: " + JSON.stringify(response));
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
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