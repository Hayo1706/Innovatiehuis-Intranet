<template>
  <div class="container">
    <div id=window>
      <h1 id=title>Projects Window</h1>
        <ProjectButton v-for="project of projects" :key="project.id"
          v-bind:projectId="project.id"
          v-bind:projectName="project.name"
          v-bind:recentUpdate="project.recentUpdate"
          v-on:reload="reload()"
        />
    </div>
  </div>
</template>

<script>
import ProjectButton from './ProjectButton.vue';

export default {
  components: { ProjectButton },
  name: "ProjectsWindow",
  props: [

  ],
  data: function () {
    return { projects: [
      {id: 1, name: "Eerste Project", recentUpdate: true},
      {id: 2, name: "Tweede Project", recentUpdate: true},
      {id: 3, name: "Derde Project", recentUpdate: false}
      ]};
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