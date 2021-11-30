<template>
  <div>
    <ProjectsHeader></ProjectsHeader>
    <div v-for="project of projects" :key="project.name">
      <ProjectListing
        @removeProject="this.removeProject"
        v-bind:project="project"
      ></ProjectListing>
    </div>
  </div>
</template>

<script>
import ProjectListing from "./ProjectListing.vue";
import ProjectsHeader from "./ProjectsHeader.vue";
import { getProjects } from "@/networkservice/networkservice.js";
export default {
  components: { ProjectListing, ProjectsHeader },
  name: "ProjectsPage",
  data: function () {
    return { projects: [] };
  },
  methods: {
    removeProject(id) {
      this.projects = this.projects.filter(function (item) {
        return item.projectid !== id;
      });
    },
  },
  async created() {
    this.$emit("loaded", "Projecten - Overzicht");
    getProjects()
      .then((response) => {
        this.projects = response;
      })
      .catch((err) => {
        console.log(err);
        alert("Network error! Connection timed out!");
      });
  },
};
</script>

<style scoped>
</style>