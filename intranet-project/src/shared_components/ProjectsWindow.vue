<template>
  <div class="component-container">
    <div class="component-header">
      <slot></slot>
      <div class="full-button" @click="toProjectsPage()">Alle Projecten</div>
      <div class="full-button" @click="toUsersPage()">Alle Gebruikers</div>
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
export default {
  components: { ProjectButton },
  name: "ProjectsWindow",
  props: [],
  data: function () {
    return { projects: [] };
  },
  async created() {
    ProjectService.getProjectsByUser(1) //TODO: get user id from session data/JWT
      .then((response) => {
        this.projects = response;
        console.log("API RESPONDS: " + response);
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
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
#projects-window {
}
.full-button {
  margin-top: 0.8vh;
  margin-right: 5px;
  padding: 5px;
  font-size: 16pt;
  font-weight: bold;
  background-color: var(--gold2);
  color: var(--blue1);
  height: 4.5vh;
  align-items: center;
  display: flex;
  cursor: pointer;
  float: right;
  box-shadow: 1vh 1vh;
}
</style>