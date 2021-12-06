<template>
  <div>
    <div class="row">
      <VerticalHeader class="d-block d-lg-none"></VerticalHeader>
      <!-- small screens-->
      <div class="col d-block d-lg-none mobileRow">
        <div class="projectButton mobileRow" @click="onClick()">
          {{ project.name }}
        </div>
        <div class="mobileRow">{{ project.createdat }}</div>
        <div>{{ project.lastupdated }}</div>
        <div class="mobileRow"><br /></div>
        <br />
        <div class="mobileRow"></div>
      </div>

      <!-- large screens-->
      <div class="projectButton col d-none d-lg-block" @click="onClick()">
        {{ project.name }}
      </div>
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
  methods: {
    onClick() {
      this.$router.push("/project/" + this.project.projectid);
    },
  },
};
</script>

<style scoped>
#projectListing {
  font-family: AddeleThin;
}
.row {
  padding-top: 12px;
}
.projectButton {
  font-weight: bold;
  background-color: var(--gold2);
  color: var(--blue1);
  border-style: outset;
  border-radius: 8px;
  padding-left: 10px;
  height: fit-content;
  box-sizing: border-box;
  cursor: pointer;
}
.mobileRow {
  height: 40px;
}
</style>