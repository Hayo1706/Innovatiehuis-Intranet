<template>
  <router-link :to="'/project/' + this.projectId" class="project-button">
    <!-- <img
      v-if="lastUpdated >= lastVisit"
      src=".\..\assets\images\logo\square.png"
    />
    <img
      v-if="lastUpdated < lastVisit"
      src=".\..\assets\images\logo\square_dark.png"
    /> -->
    <label class="project-name">{{ this.projectName }}</label>
  </router-link>
</template>

<script>
export default {
  name: "AnnouncementWindow",
  props: ["projectId", "projectName", "lastUpdated"],
  data: function () {
    return {
      lastVisit: new Date(),
    };
  },
};
</script>


<style scoped>
.project-button {
  box-sizing: border-box;
  margin-left: 10px;
  margin-top: 2vh;
  font-size: 16pt;
  background: white;
  border-radius: 0 1rem 1rem 0;
  color: #546472;
  text-decoration: none;
  width: 95%;
  height: 10vh;
  align-items: center;
  display: flex;
  cursor: pointer;
  border: transparent;
  border-left: solid var(--gold1) 8px;
  -webkit-transition: .3s;
  transition: .3s;
}
.project-button:hover {
  border-left: solid var(--gold1) 18px;
  -webkit-transition: .3s;
  transition: .3s;
}
.project-name {
  font-size: 20pt;
  margin: 16px;
}
img {
  height: 5vh;
  padding-right: 8px;
  cursor: pointer;
}
</style>