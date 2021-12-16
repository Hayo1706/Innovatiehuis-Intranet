<template>
    <div class="projectFolder" @click="goToDirectory(this.path)">
        <img class="foldersImage" v-if="this.shared != 'yes'" src=".\..\..\assets\images\folder.png"/> 
        <img class="foldersImage" v-if="this.shared == 'yes'" src=".\..\..\assets\images\shared_folder.png"/> 
        {{this.naam}}
    </div>
</template>

<script>
export default {
  name: "ProjectFolder",
  props: {
    naam: { type: String, required: true },
    path: { type: String, required: true },
    shared: { type: String, required: true },
  },
  data: function () {
    return {
    };
  },
  methods: {
    goToDirectory(path) {
       this.$router.push(this.$route.params.id + "/" + path);
    },
  }
};
</script>

<style scoped>
.foldersImage {
  height: calc(2vw + 5vh);
  padding-right: 1vw;
  padding-bottom: 0.5vh;
}
.projectFolder {
  color: white;
}
</style>