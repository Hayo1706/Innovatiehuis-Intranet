<template>
  <header v-if="this.$route.path !== '/login'">
    <div id="header-container">
      <div class="image-container align-left-header">
        <img 
          title="Hoofdpagina"
          class="logo" 
          @click="logoClick()" 
          src=".\..\assets\images\logo\square.png" 
        />
        <img 
          data-toggle="tooltip" data-placement="bottom" title="Projectenoverzicht"
          class="header-icon"
          @click="projectsClick()"
          src=".\..\assets\images\projects_icon_yellow.png"
          v-if="this.canSeeProjects()"
        />
        <img
          title="Gebruikersoverzicht"
          class="header-icon"
          @click="usersClick()"
          src=".\..\assets\images\users_icon_yellow.png"
          v-if="this.canSeeUsers()"
        />
      </div>
      <div class="image-container .align-middle-header">
        <img
          title="Projectgegevens"
          class="header-icon"
          @click="settingClick()"
          src=".\..\assets\images\gear_icon3.png"
          v-if="this.$route.path.indexOf('/project/') > -1"
        />
        <slot style="margin: 10vw;"></slot>
      </div>

      <div class="image-container align-right-header">
        <img 
          title="Profiel"
          class="header-icon" 
          @click="profileClick()" 
          src=".\..\assets\images\profile_icon.png" 
        />
        <img 
          title="Uitloggen"
          class="header-icon" 
          @click="logout()" 
          src=".\..\assets\images\logout-icon.png" 
        />
      </div>
    </div>
  </header>
</template>

<script>
import LoginService from "../services/LoginService";
import PermissionService from "../services/PermissionService";

export default {
  name: "AppHeader",
  props: ["header_title"],
  data: function () {
    return {};
  },
  methods: {
    logoClick() {
      this.$router.push("/home");
    },
    projectsClick() {
      this.$router.push("/manage/projects");
    },
    usersClick() {
      this.$router.push("/manage/users");
    },
    profileClick() {
      this.$router.push("/user/" + localStorage.getItem("userid"));
    },
    logout() {
      LoginService.logout();
      this.$router.push("/login");
    },
    settingClick() {
      this.$router.push(
        "/project/" + this.$route.params.id + "/projectsettings"
      );
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
img {
  height: 80%;
  cursor: pointer;
}
header {
  width: 100%;
  padding-top: 1vh;
  height: 11vh;
  margin-bottom: 2vh;
  background: rgba(255, 255, 255, 0.9);
  border-bottom: solid 2px var(--gold1);
}

#header-container {
  color: var(--blue1);
  font-size: min(calc(10px + 2vw), 36px);
  display: flex;
  justify-content: space-around;
  align-items: center;
  max-width: 1500px;
  margin: auto;
  height: 9vh;
}
.image-container {
  padding: 0;
  margin: 0;
  height: 100%;
  align-items: center;
  display: flex;
}
.options {
  height: 70%;
}

.align-right-header{
  margin-left: auto;
  margin-right: 1.5vw;
}

.align-left-header{
  margin-right: auto;
  margin-left: calc(0.5vw + 10px);
}

.align-middle-header{
  margin-left: auto;
  margin-right: auto;
}

.header-icon {
  box-sizing: content-box;
  margin: 0 1vh;
  border-radius: 50%;
}

.header-icon:hover {
  box-shadow: 0 0 0 3px rgba(186, 186, 186, 0.9)
  /* border: 4px solid grey; */
}

.logo{
  margin-right: 2vh;
}
</style>
