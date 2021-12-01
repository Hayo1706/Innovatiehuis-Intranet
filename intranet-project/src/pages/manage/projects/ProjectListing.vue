<template>
  <div>
    <div class="row">
      <VerticalHeader class="d-block d-lg-none"></VerticalHeader>
      <!-- small screens-->
      <div class="col d-block d-lg-none">
        <div>{{ project.name }}</div>
        <div>{{ project.createdat }}</div>
        <div>{{ project.lastupdated }}</div>
        <div><br /></div>
        <div></div>
      </div>

      <!-- large screens-->
      <div class="col d-none d-lg-block">{{ project.name }}</div>
      <div class="col d-none d-lg-block">{{ project.createdat }}</div>
      <div class="col d-none d-lg-block">{{ project.lastupdated }}</div>
      <div class="col d-none d-lg-block"><br /></div>
      <div class="col d-none d-lg-block"></div>

      <div class="col">
        <ProjectButtons
          @removeProject="(id) => $emit('removeProject', id)"
          @archiveProject="(_project) => $emit('archiveProject', _project)"
          v-bind:project="project"
        ></ProjectButtons>
      </div>
    </div>
    <hr />
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