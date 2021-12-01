<template>
  <div class="col">
    <img src="@/assets/images/users_icon.png" class="d-block d-lg-inline" />
    <img
      v-if="project.isarchived"
      src="https://cdn-icons-png.flaticon.com/512/60/60723.png"
      class="d-block d-lg-inline"
      @click="handleArchiveProject(project)"
    />
    <img
      v-else
      src="https://www.pngkey.com/png/full/876-8761970_download-button-comments-icon-png-archive-icon.png"
      class="d-block d-lg-inline"
      @click="handleArchiveProject(project)"
    />
    <img
      src="https://www.pngrepo.com/png/320601/512/crossed-pistols.png"
      class="d-block d-lg-inline"
      @click="handleDeleteProject(project)"
    />
  </div>
</template>

<script>
import {
  deleteProject,
  updateProject,
} from "@/services/ProjectService.js";

export default {
  props: ["project"],
  components: {},
  name: "ProjectButtons",
  data: function () {
    return {};
  },
  methods: {
    async handleDeleteProject(project) {
      let answer = confirm(
        "Wil je het project " + project.name + " echt verwijderen?"
      );
      if (answer) {
        deleteProject(project.projectid)
          .then(() => {
            //remove the project from the view
            this.$emit("removeProject", project.projectid);
          })
          .catch((err) => {
            //invalid operation on server
            if (err.response) {
              console.log(err.response.status);
              alert(err);
            } else {
              alert("Network error! Connection timed out!");
            }
          });
      }
    },
    async handleArchiveProject(project) {
      let projectCopy = JSON.parse(JSON.stringify(project));
      projectCopy.isarchived = !projectCopy.isarchived;
      updateProject(projectCopy)
        .then(() => {
          project.isarchived = !project.isarchived;
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
            alert(err);
          } else {
            alert("Network error! Connection timed out!");
          }
        });
    },
  },
};
</script>
<style scoped>
img {
  max-width: 70px;
  margin-right: 10px;
  cursor: pointer;
}
</style>