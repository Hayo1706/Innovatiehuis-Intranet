<template>
  <div class="component-container" style="min-height: fit-content">
    <div class="component-header">
      <slot></slot>
    </div>
    <div>
      <button
          data-toggle="tooltip" data-placement="bottom" title="Projectenoverzicht"
          class="full-button mobileRow extraLarge"
          @click="projectsClick()"
          v-if="this.canSeeProjects()"

      ><img src="../../assets/images/projects_icon.png">Projectenoverzicht</button>
      <button
          title="Gebruikersoverzicht"
          class="full-button mobileRow extraLarge"
          @click="usersClick()"
          v-if="this.canSeeUsers()"
      ><img src="../../assets/images/users_icon.png">Gebruikersoverzicht</button>
      <hr>
      <button
          title="Gebruikersoverzicht"
          class="full-button mobileRow extraLarge"
          @click="usersClick()"
          v-if="this.canSeeUsers()"
      >Project aanmaken</button>
      <button
          title="Gebruikersoverzicht"
          class="full-button mobileRow extraLarge"
          @click="usersClick()"
          v-if="this.canSeeUsers()"
      >Gebruiker toevoegen</button>
    </div>
  </div>
</template>

<script>
import PermissionService from "@/services/PermissionService";

export default {
  components: {  },
  name: "AdminView",
  props: [],
  data: function () {
    return {
    };
  },
  methods: {
    projectsClick() {
      this.$router.push("/manage/projects");
    },
    usersClick() {
      this.$router.push("/manage/users");
    },
    canSeeProjects() {
      return (
          PermissionService.userHasPermission('may_read_any_project')
      )
    },
    canSeeUsers() {
      return (
          PermissionService.userHasPermission('may_read_any_user')
      )
    }
  },
};
</script>

<style scoped>
button:hover{
  padding-left: 15px;

}
img{
  height: 40px;
  margin-right: 20px;
  margin-left: 20px;
}
</style>