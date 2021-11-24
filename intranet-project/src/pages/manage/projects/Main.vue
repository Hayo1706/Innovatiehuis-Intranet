<template>
  <div>
    <div id="descriptionbar" class="d-none d-lg-flex">
      <span>Project</span>
      <span>Aangemaakt</span>
      <span>Laatste Update</span
      ><span
        >Overkoepelend<br />
        project</span
      >
      <span>Sub-projecten</span>
      <span></span>
    </div>
    <div id="projectlist" v-for="project of projects" :key="project.name">
      <ProjectListing
        v-bind:id="project.projectid"
        v-bind:name="project.name"
        v-bind:created="project.createdat"
        v-bind:lastModified="project.lastupdated"
        v-bind:isArchived="project.isarchived"
        v-on:reload="reload()"
      />
      <br />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ProjectListing from './ProjectListing.vue';

export default {
  components: { ProjectListing },
  name: "ProjectsPage",
  data: function () {
    return { projects: [] };
  },
  methods: {
    reload() {
      axios
        .get("http://94.212.125.203:5000/api/projects")
        .then((response) => {
          this.projects = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  created() {
    this.reload();
    this.$emit("loaded", "Projecten - Overzicht");
  },
};
</script>

<style>
#descriptionbar {
  width: 100%;
  box-sizing: border-box;
  min-height: 10vh;
  background-color: #28418a;
  border: white 5px solid;
  margin-top: 1vh;
  color: white;
  font-size: calc(1vw + 1vh);
  padding: 20px;

  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-basis: 100%;
  gap: 60px;
  font-family: AddeleSemiBold;
}

#projectlist {
  width: 100%;
  box-sizing: border-box;
  border-left: white 5px solid;
  border-right: white 5px solid;
  color: white;
  font-size: calc(1vw + 1vh);
  padding: 1vw;
  font-family: AddeleThin;
}

span {
  flex: 1 1 0;
  width: 0;
  overflow-wrap: anywhere;
}
</style>