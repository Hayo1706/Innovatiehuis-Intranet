<template>
  <ConfirmDialogue ref="confirmDialogue"></ConfirmDialogue>

  <div class="col">
    <div class="row" style="margin-right: 8px;">
      <div class="col">
        <div v-show="canArchive()">
          <div v-if="project.is_archived" class="link" @click="handleArchiveProject(project)">
            <span title="Project de-archiveren" class="listing-icon icon-holder">
              <img src="@/assets/images/dearchive.png" />
            </span>
          </div>
          <div v-else class="link" @click="handleArchiveProject(project)">
            <span title="Project archiveren" class="listing-icon icon-holder">
              <img src="@/assets/images/archive.png" />
            </span>
          </div>
        </div>
      </div>

      <div class="col">
        <div class="link" v-show="canDelete()" @click="handleDeleteProject(project)">
          <span title="Project verwijderen" class="listing-icon icon-holder">
            <img src="@/assets/images/delete.png" />
          </span>
        </div>
      </div>
    </div>
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
        title: action[0].toUpperCase() + action.substring(1),
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
.col {
  padding: 0;
}
img {
  height: 3em;
  cursor: pointer;
  opacity: 60%;
}
img:hover {
  opacity: 80%;
}
.rotate {
  transform: rotate(180deg);
}
.link {
  text-decoration: none;
}
.icon-holder {
  display: inline-block;
}
</style>