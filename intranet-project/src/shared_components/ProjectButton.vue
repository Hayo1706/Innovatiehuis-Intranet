<template>
    <button @click="onClick()" id="project-button">
      <img v-if="recentUpdate" src=".\..\assets\images\logo\square.png" style="position:absolute;left:15px;" />
      {{ this.projectName }}
    </button>
</template>

<script>
export default {
  name: "AnnouncementWindow",
  props: [

  ],
  data: function () {
    return {
        projectId:1,
        projectName:"Testproject",
        recentUpdate:true
    };
  },
  methods: {
      onClick() {
        this.$router.push("/project/" + this.projectId)
      }
  }
}
</script>


<style scoped>
#project-button {
    font-size: 16pt;
    font-weight: bold;
    background-color: #c6992f;
    color: #28418A;
    width: 300px;
    height: 60px;
    border-style: outset;
    text-align: center;
    justify-content: center;
    align-items: center;
    display: flex;
    border-radius: 8px;
}
</style>