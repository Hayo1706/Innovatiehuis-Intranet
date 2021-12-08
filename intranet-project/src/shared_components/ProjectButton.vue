<template>
  <button @click="onClick()" class="project-button">
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
.project-button {
  padding: 10px;
  margin: 10px;
  font-size: 16pt;
  font-weight: bold;
  background-color: var(--gold2);
  color: var(--blue1);
  width: 100%;
  height: 12vh;
  border-style: outset;
  align-items: center;
  display: flex;
  border-radius: 8px;
  cursor: pointer;
}
img {
  height: 5vh;
  padding-right: 8px;
  cursor: pointer;
}
</style>