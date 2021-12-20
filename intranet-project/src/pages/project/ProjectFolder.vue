<template>
    <div class="projectFolder" @click="goToDirectory(this.path)" v-on:click.right="deleteDirectory(true)">
        <img class="foldersImage" v-if="this.shared != 'yes'" src=".\..\..\assets\images\folder.png"/> 
        <img class="foldersImage" v-if="this.shared == 'yes'" src=".\..\..\assets\images\shared_folder.png"/> 
        {{this.naam}}
    </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
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
    deleteDirectory(confirmation){
      FilestorageService.deleteFolder(
        this.$route.params.id, 
        this.naam,
        this.$route.fullPath,
        confirmation
      ).then((response) => {
          alert(response);
          console.log(response);
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
          alert(err);
        });
    },
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