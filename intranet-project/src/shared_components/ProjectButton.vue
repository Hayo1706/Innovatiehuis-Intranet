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
  box-sizing: border-box;
  margin-left: 10px;
  margin-top: 2vh;
  font-size: 16pt;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 0 1rem 1rem 0;
  color: var(--blue1);
  width: 95%;
  height: 10vh;
  align-items: center;
  display: flex;
  cursor: pointer;
  border: transparent;
  border-left: solid var(--gold1) 2px;

}
img {
  height: 5vh;
  padding-right: 8px;
  cursor: pointer;
}
</style>