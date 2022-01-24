<template>
  <header v-if="!this.$route.path.includes('/login')">
    <div id="header-container">
      <div class="image-container align-left-header">
        <router-link to="/home">
          <img 
            title="Hoofdpagina"
            id="logo" 
            src=".\..\assets\images\logo\square.png" 
          />
        </router-link>
        <router-link class="link" to="/manage/projects" v-if="this.canSeeProjects()">
          <img 
            data-toggle="tooltip" data-placement="bottom" title="Projectenoverzicht"
            class="header-icon"
            src=".\..\assets\images\projects_icon_yellow.png"
          />
        </router-link>
        <router-link to="/manage/users" v-if="this.canSeeUsers()">
          <img
            title="Gebruikersoverzicht"
            class="header-icon"
            src=".\..\assets\images\users_icon_yellow.png"
          />
        </router-link>
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
        <router-link :to="'/user/' + getUserId()">
          <img 
            title="Profiel"
            class="header-icon" 
            src=".\..\assets\images\profile_icon.png" 
          />
        </router-link>
        <a>
          <img 
            title="Uitloggen"
            class="header-icon" 
            style="margin: 0;"
            @click="logout()" 
            src=".\..\assets\images\logout-icon.png" 
          />
        </a>
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
    getUserId() {
      return localStorage.getItem("userid");
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
.link {

}
img {
  height: 7vh;
  cursor: pointer;
}
header {
  width: 100%;
  height: 100%;
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

#logo{
  height: 7vh;
  margin-right: 2vh;
}
</style>
