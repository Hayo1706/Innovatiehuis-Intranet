<template>
  <div>
    <ProjectsHeader></ProjectsHeader>
    <div v-for="project of projects" :key="project.name">
      <ProjectListing v-bind:project="project"></ProjectListing>
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
    return { projects: [{ name: "Blockchain", isArchived: true }] };
  },
  methods: {},
  async created() {
    this.$emit("loaded", "Projecten - Overzicht");
    this.projects = getProjects();
  },
};
</script>

<style scoped>
</style>