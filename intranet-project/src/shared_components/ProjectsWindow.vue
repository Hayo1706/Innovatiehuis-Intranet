<template>
  <div class="component-container">
    <div class="component-header">
      <slot></slot>
      <div class="full-button" @click="toProjectsPage()">Alle Projecten</div>
      <div class="full-button" @click="toUsersPage()">Alle Gebruikers</div>
    </div>
    
    <div id="project-window" class="component-body">
      <ProjectButton
        v-for="project of projects"
        :key="project.id"
        v-bind:projectId="project.projectid"
        v-bind:projectName="project.name"
        v-bind:lastUpdated="project.lastupdated"
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
    }
  }
};
</script>

<style scoped>
#project-window {

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
  border-style: outset;
  border-width: 2px;
  align-items: center;
  display: flex;
  border-top-left-radius: 2vh;
  border-top-right-radius: 2vh;
  cursor: pointer;
  float: right;
}
</style>