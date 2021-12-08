<template>
  <div class="col">
    <img
      src="@/assets/images/users_icon.png"
      class="d-block d-lg-inline"
      @click="gotoMembers()"
    />
    <img
      v-if="project.isarchived"
      src="@/assets/images/upload.png"
      class="d-block d-lg-inline"
      @click="handleArchiveProject(project)"
    />
    <img
      v-else
      src="@/assets/images/archive.png"
      class="d-block d-lg-inline"
      @click="handleArchiveProject(project)"
    />
    <img
      src="@/assets/images/blackx.png"
      class="d-block d-lg-inline"
      @click="handleDeleteProject(project)"
    />
  </div>
</template>

<script>
export default {
  props: ["project"],
  components: {},
  name: "ProjectButtons",
  data: function () {
    return {};
  },
  methods: {
    gotoMembers() {
      this.$router.push({ path: `/project/${this.project.projectid}/members` });
    },
    async handleDeleteProject(project) {
      let answer = confirm(
        'Wil je het project "' + project.name + '" echt verwijderen?'
      );
      if (answer) {
        this.$emit("removeProject", project.projectid);
      }
    },
    async handleArchiveProject(project) {
      let action = "archiveren";
      if (project.isarchived) {
        action = "zichtbaar maken";
      }
      let answer = confirm(
        'Wil je het project "' + project.name + '" echt ' + action + "?"
      );
      if (answer) {
        this.$emit("archiveProject", project);
      }
    },
  },
};
</script>
<style scoped>
img {
  max-width: 70px;
  margin: 4px;
  cursor: pointer;
}
</style>