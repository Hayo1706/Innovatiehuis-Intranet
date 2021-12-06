<template>
  <button @click="onClick()" id="project-button">
    <img
      v-if="lastUpdated >= lastVisit"
      src=".\..\assets\images\logo\square.png"
    />
    <img
      v-if="lastUpdated < lastVisit"
      src=".\..\assets\images\logo\square_dark.png"
    />
    {{ this.projectName }}
  </button>
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
  methods: {
    onClick() {
      this.$router.push("/project/" + this.projectId);
    },
  },
};
</script>


<style scoped>
#project-button {
  font-size: 16pt;
  font-weight: bold;
  background-color: var(--gold2);
  color: var(--blue1);
  width: 300px;
  height: 60px;
  border-style: outset;
  align-items: center;
  display: flex;
  border-radius: 8px;
}
img {
  height: 5vh;
  padding-right: 8px;
  cursor: pointer;
}
</style>