<template>
  <div class="col">
    <div id="archivedText" v-if="project.is_archived">Gearchiveerd</div>
    <a class="link" @click="gotoMembers()">Leden</a>
    <a
      v-if="project.is_archived"
      src="@/assets/images/upload.png"
      class="link"
      @click="handleArchiveProject(project)"
      >Dearchiveren</a
    >
    <a v-else class="link" @click="handleArchiveProject(project)">Archiveren</a>
    <a class="link" @click="handleDeleteProject(project)">Verwijderen</a>
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
        'Wil je het project "' + project.project_name + '" echt verwijderen?'
      );
      if (answer) {
        this.$emit("removeProject", project.projectid);
      }
    },
    async handleArchiveProject(project) {
      let action = "archiveren";
      if (project.is_archived) {
        action = "dearchiveren";
      }
      let answer = confirm(
        'Wil je het project "' + project.project_name + '" echt ' + action + "?"
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
#archivedText {
  margin-bottom: 10px;
  color: purple;
}
</style>