<template>
  <div>
    <ProjectsHeader></ProjectsHeader>
    <ProjectListing></ProjectListing>
    <ProjectListing></ProjectListing>
  </div>
</template>

<script>
import ProjectListing from "./ProjectListing.vue";
import ProjectsHeader from "./ProjectsHeader.vue";
export default {
  components: { ProjectListing, ProjectsHeader },
  name: "ProjectsPage",
  data: function () {
    return { projects: [] };
  },
  methods: {},
  created() {
    this.$emit("loaded", "Projecten - Overzicht");
  },
};
</script>

<style scoped>
</style>