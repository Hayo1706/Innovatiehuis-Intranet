<template>
  <div class="col">
    <a class="link" @click="gotoMembers()">Leden</a>
    <a
      v-if="project.isarchived"
      src="@/assets/images/upload.png"
      class="link"
      @click="handleArchiveProject(project)"
    >Dearchiveren</a>
    <a
      v-else
      class="link"
      @click="handleArchiveProject(project)"
    >Archiveren</a>
    <a
      class="link"
      @click="handleDeleteProject(project)"
    >Verwijderen</a>
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
        action = "dearchiveren maken";
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
.link {
  cursor: pointer;
  color: var(--gold2);
  display: block;
  margin-bottom: 10px;
  text-decoration: none;
}
</style>