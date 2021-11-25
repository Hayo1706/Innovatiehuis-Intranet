<template>
  <div>
    <!-- for larger screens-->
    <div id="projectListing" class="container-fluid d-none d-lg-block">
      <div class="row">
        <div class="col">{{ project.name }}</div>
        <div class="col">{{ project.createdat }}</div>
        <div class="col">{{ project.lastupdated }}</div>
        <div class="col"></div>
        <div class="col"></div>
        <ProjectButtons v-bind:project="project"></ProjectButtons>
      </div>
      <hr />
    </div>

    <!-- for smaller screens-->
    <div id="projectListing" class="container-fluid d-sm-block d-lg-none">
      <div class="row">
        <VerticalHeader></VerticalHeader>
        <div class="col">
          <div>{{ project.name }}</div>
          <div>{{ project.createdat }}</div>
          <div>{{ project.lastupdated }}</div>
          <div><br /></div>
          <div></div>
        </div>

        <div class="col">
          <ProjectButtons v-bind:project="project"></ProjectButtons>
        </div>
      </div>
      <hr />
    </div>
  </div>
</template>

<script>
import VerticalHeader from "./VerticalHeader.vue";
import ProjectButtons from "./ProjectButtons.vue";
export default {
  props: ["project"],
  components: { VerticalHeader, ProjectButtons },
  name: "ProjectListing",
  data: function () {
    return {};
  },
  methods: {},
};
</script>

<style scoped>
#projectListing {
  font-family: AddeleThin;
}
.row {
  padding-top: 12px;
}
</style>