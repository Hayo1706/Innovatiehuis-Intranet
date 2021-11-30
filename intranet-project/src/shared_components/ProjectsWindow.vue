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
import Axios from 'axios';

export default {
  components: { ProjectButton },
  name: "ProjectsWindow",
  props: [
    
  ],
  data: function () {
    return { projects: []};
  },
  created: function() {
    Axios
      .get("http://127.0.0.1:5000/api/user/1/projects") // TODO: use network service
      .then((response) => {
        console.log('Received data from api/projects');
        this.projects = response.data;
      })
      .catch((error) => {
        console.log(error);
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