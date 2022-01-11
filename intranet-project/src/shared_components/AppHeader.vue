<template>
  <header v-if="this.$route.path !== '/login'">
    <div id="header-container">
      <div class="image-container">
        <img class="logo" @click="logoClick()" src=".\..\assets\images\logo\square.png" />
        <img
          class="header-icon"
          @click="projectsClick()"
          src=".\..\assets\images\projects_icon.png"
          v-if="this.canSeeProjects()"
        />
        <img
          class="header-icon"
          @click="usersClick()"
          src=".\..\assets\images\users_icon.png"
          v-if="this.canSeeUsers()"
        />
      </div>
      <div class="image-container">
        <img
          class="header-icon"
          @click="settingClick()"
          src=".\..\assets\images\gear_icon3.png"
          v-if="this.$route.path.indexOf('/project/') > -1"
        />
        <slot style="margin: 10vw;"></slot>
      </div>

      <div class="image-container">
        <img class="header-icon" @click="profileClick()" src=".\..\assets\images\profile_icon.png" />
        <img class="header-icon" @click="logout()" src=".\..\assets\images\logout-icon.png" />
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
  height: 9vh;
  margin-top: 3vh;
  margin-bottom: 2vh;
  /*background-color: var(--blue1);*/
  background: linear-gradient(
    to bottom right,
    rgba(255, 255, 255, 0.8),
    rgba(225, 225, 225, 0.9)
  );
  backdrop-filter: blur(1rem);
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
.header-icon {
  border-style: outset;
  border-radius: 50%;
}

.header-icon:hover {
  border-style: ridge;
}
</style>
