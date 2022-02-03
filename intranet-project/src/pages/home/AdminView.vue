<template>
  <div id="AdminView" class="component-container" v-if="canSeeAdminView()">
    <div class="component-header">
      <slot></slot>
    </div>
    <div>
      <router-link
        title="Projectenoverzicht"
        class="full-button mobileRow extraLarge"
        to="/manage/projects"
        v-if="this.canSeeProjects()"
      >
        <img class="big-img" src="../../assets/images/projects_icon.png" />Projectenoverzicht
      </router-link>
      <router-link
        title="Gebruikersoverzicht"
        class="full-button mobileRow extraLarge"
        to="/manage/users"
        v-if="this.canSeeUsers()"
      >
        <img class="big-img" src="../../assets/images/users_icon.png" />Gebruikersoverzicht
      </router-link>
      <router-link
          title="Rollenoverzicht"
          class="full-button mobileRow extraLarge"
          to="/manage/roles"
          v-if="this.canSeeUsers()"
      >
        <img class="big-img" src="../../assets/images/roles_icon.png" />Rollenoverzicht
      </router-link>
      <hr />
      <button
        title="Nieuw project aanmaken"
        class="full-button mobileRow extraLarge"
        data-bs-target="#createProjectModal"
        data-bs-toggle="modal"
        type="button"
        v-if="this.canCreateProjects()"
      >
        <img class="small-img" src="../../assets/images/add_project.png" />
        Nieuw project
      </button>
      <button
        title="Nieuwe gebruiker toevoegen"
        class="full-button mobileRow extraLarge"
        data-bs-target="#createUserModal"
        data-bs-toggle="modal"
        type="button"
        v-if="this.canCreateUsers()"
      >
        <img class="small-img" src="../../assets/images/add_user.png" />
        Nieuwe gebruiker
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
    canSeeProjects() {
      return PermissionService.userHasPermission("may_read_any_project");
    },
    canSeeUsers() {
      return PermissionService.userHasPermission("may_read_any_user");
    },
    canCrudRoles(){
      return PermissionService.userHasPermission("may_crud_roles")
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
#AdminView {
  min-height: fit-content;
}
button:hover {
  padding-left: 15px;
}
.big-img {
  height: 40px;
  margin-right: 16px;
  margin-left: 4px;
}
.small-img{
  height: 30px;
  margin-right: 12px;
  margin-left: 4px;
}
</style>