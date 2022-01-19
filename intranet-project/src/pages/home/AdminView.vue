<template>
  <div class="component-container" style="min-height: fit-content" v-if="canSeeAdminView()">
    <div class="component-header">
      <slot></slot>
    </div>
    <div>
      <button
        data-toggle="tooltip"
        data-placement="bottom"
        title="Projectenoverzicht"
        class="full-button mobileRow extraLarge"
        @click="projectsClick()"
        v-if="this.canSeeProjects()"
      >
        <img src="../../assets/images/projects_icon.png" />Projectenoverzicht
      </button>
      <button
        title="Gebruikersoverzicht"
        class="full-button mobileRow extraLarge"
        @click="usersClick()"
        v-if="this.canSeeUsers()"
      >
        <img src="../../assets/images/users_icon.png" />Gebruikersoverzicht
      </button>
      <button
          title="Rollenoverzicht"
          class="full-button mobileRow extraLarge"
          @click="rolesClick()"
          v-if="this.canSeeUsers()"
      >
        <img src="../../assets/images/users_icon.png" />Rollenoverzicht
      </button>
      <hr />
      <button
        title="Project aanmaken"
        class="full-button mobileRow extraLarge"
        data-bs-target="#createProjectModal"
        data-bs-toggle="modal"
        type="button"
        v-if="this.canCreateProjects()"
      >
        <img src="../../assets/images/add_project.png" />Project aanmaken
      </button>
      <button
        title="Gebruiker aanmaken"
        class="full-button mobileRow extraLarge"
        data-bs-target="#createUserModal"
        data-bs-toggle="modal"
        type="button"
        v-if="this.canCreateUsers()"
      ><img src="../../assets/images/add_user.png" />
        Gebruiker toevoegen
      </button>
    </div>
    <ProjectCreateModal></ProjectCreateModal>
    <UserCreateModal></UserCreateModal>
  </div>
</template>

<script>
import PermissionService from "@/services/PermissionService";
import ProjectCreateModal from "@/pages/manage/projects/ProjectCreateModal.vue";
import UserCreateModal from "@/pages/manage/users/UserCreateModal.vue";
export default {
  components: { ProjectCreateModal, UserCreateModal },
  name: "AdminView",
  props: [],
  data: function () {
    return {};
  },
  methods: {
    projectsClick() {
      this.$router.push("/manage/projects");
    },
    usersClick() {
      this.$router.push("/manage/users");
    },
    rolesClick() {
      this.$router.push("/manage/roles")
    },
    canSeeProjects() {
      return PermissionService.userHasPermission("may_read_any_project");
    },
    canSeeUsers() {
      return PermissionService.userHasPermission("may_read_any_user");
    },
    canCreateProjects() {
      return PermissionService.userHasPermission("may_create_project");
    },
    canCreateUsers() {
      return PermissionService.userHasPermission("may_create_users");
    },
    canSeeAdminView(){
      return this.canSeeProjects() || this.canSeeUsers() || this.canCreateProjects() ||this.canCreateUsers()
    }
  },
};
</script>

<style scoped>
button:hover {
  padding-left: 15px;
}
img {
  height: 40px;
  margin-right: 20px;
  margin-left: 20px;
}
.component-container button img{
  height: 30px;
  margin-right: 12px;
  margin-left: 4px;
}
</style>