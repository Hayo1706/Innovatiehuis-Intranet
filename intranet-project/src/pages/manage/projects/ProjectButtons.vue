<template>
  <div class="col">
    <ConfirmDialogue ref="confirmDialogue"></ConfirmDialogue>
    <span v-show="canArchive()">
      <a
        v-if="project.is_archived"
        src="@/assets/images/upload.png"
        class="link"
        @click="handleArchiveProject(project)"
        >Dearchiveren</a
      >

      <a v-else class="link" @click="handleArchiveProject(project)"
        >Archiveren</a
      >
    </span>
    <a class="link" v-show="canDelete()" @click="handleDeleteProject(project)"
      >Verwijderen</a
    >
  </div>
</template>

<script>
import PermissionService from "@/services/PermissionService.js";
import ConfirmDialogue from "@/shared_components/ConfirmDialogue.vue";

export default {
  props: ["project"],
  components: { ConfirmDialogue },
  name: "ProjectButtons",
  data: function () {
    return {};
  },
  methods: {
    canArchive() {
      return PermissionService.userHasPermission("may_archive_any_project");
    },
    canDelete() {
      return PermissionService.userHasPermission("may_delete_any_project");
    },
    async handleDeleteProject(project) {
      const ok = await this.$refs.confirmDialogue.show({
        title: "Verwijderen",
        message:
          'Wil je het project "' + project.project_name + '" echt verwijderen?',
      });
      if (ok) {
        this.$emit("removeProject", project.projectid);
      }
    },
    async handleArchiveProject(project) {
      let action = "archiveren";
      if (project.is_archived) {
        action = "dearchiveren";
      }

      const ok = await this.$refs.confirmDialogue.show({
        title: "Archiveren",
        message:
          'Wil je het project "' +
          project.project_name +
          '" echt ' +
          action +
          "?",
      });
      // If you throw an error, the method will terminate here unless you surround it wil try/catch
      if (ok) {
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