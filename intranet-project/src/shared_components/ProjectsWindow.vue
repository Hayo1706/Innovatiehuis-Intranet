<template>
  <div class="component-container">
    <div class="component-header">
      <slot></slot>
    </div>
    <div class="full-button" @click="toProjectsPage()" v-if="this.archivePermission">Alle Projecten</div>
    <div class="full-button" @click="toUsersPage()">Alle Gebruikers</div>

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
export default {
  components: { ProjectButton },
  name: "ProjectsWindow",
  props: [],
  data: function () {
    return { 
      projects: [],
      archivePermission: false
      };
  },
  async created() {
    this.archivePermission = localStorage.getItem('may_archive_any_project') == "1";
    ProjectService.getProjectsByUser(localStorage.getItem('userid'))
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