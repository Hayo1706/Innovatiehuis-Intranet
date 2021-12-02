<template>
  <div class="container">
    <div id=window>
      <h1 id=title>Projects Window</h1>
        <ProjectButton v-for="project of projects" :key="project.id"
          v-bind:projectId="project.projectid"
          v-bind:projectName="project.name"
          v-bind:lastUpdated="project.lastupdated"
          v-on:reload="reload()"
        />
    </div>
  </div>
</template>

<script>
import ProjectButton from './ProjectButton.vue';
import { getProjectsForUser } from "@/services/ProjectService.js";

export default {
  components: { ProjectButton },
  name: "ProjectsWindow",
  props: [
    
  ],
  data: function () {
    return { projects: []};
  },
  async created() {
    getProjectsForUser(1) //TODO: get user id from session data/JWT
      .then((response) => {
        this.projects = response;
      })
      .catch((err) => {
        console.log(err);
        if (!err.response) {
          alert("Network error! Connection timed out!");
        }
      });
  },
}
</script>


<style scoped>
#window {
    border-style: outset;
}
#title {
  color: white;
  font-size: calc(2vw + 2vh);
  margin: 0;
  text-align: center;
  background-color: var(--blue4);
  }
</style>