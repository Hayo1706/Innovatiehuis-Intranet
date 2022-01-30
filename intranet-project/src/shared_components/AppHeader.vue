<template>
  <header v-if="!this.$route.path.includes('/login')">
    <div id="header-container">
      <router-link to="/home" v-if="canSeePages()">
        <img
          title="Hoofdpagina"
          src=".\..\assets\images\logo\square.png"
          class="home-img"
        />
      </router-link>

      <router-link
        :to="'/project/' + this.$route.params.id + '/projectsettings'"
      >
        <img
          title="Projectgegevens"
          src=".\..\assets\images\gear_icon3.png"
          v-if="this.$route.path.indexOf('/project/') > -1 && canSeePages()"
        />
      </router-link>

      <slot></slot>

      <div>
        <router-link
          class="link"
          to="/manage/projects"
          v-if="this.canSeeProjects() && canSeePages()"
        >
          <img
            data-toggle="tooltip"
            data-placement="bottom"
            title="Projectenoverzicht"
            class="header-icon"
            src=".\..\assets\images\projects_icon_yellow.png"
          />
        </router-link>
        <router-link
          to="/manage/users"
          v-if="this.canSeeUsers() && canSeePages()"
        >
          <img
            title="Gebruikersoverzicht"
            class="header-icon"
            src=".\..\assets\images\users_icon_yellow.png"
          />
        </router-link>

        <router-link :to="'/user/' + getUserId()" v-if="canSeePages()">
          <img title="Profiel" src=".\..\assets\images\profile_icon.png" />
        </router-link>
        <a>
          <img
            title="Uitloggen"
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
    canSeePages() {
      return localStorage.getItem("access_status") == 1;
    },
    canSeeProjects() {
      return PermissionService.userHasPermission("may_read_any_project");
    },
    canSeeUsers() {
      return PermissionService.userHasPermission("may_read_any_user");
    },
  },
};
</script>


<style scoped>
img {
  cursor: pointer;
  border-radius: 50%;
  height: 7vh;
  margin: 10px;
}
img:hover {
  box-shadow: 0 0 0 3px var(--blue3);
}
.title {
  flex-grow: 4;
  text-align: center;
  margin: auto;
}

header {
  width: 100%;
  height: 9vh;
  margin-bottom: 2vh;
  background: rgba(255, 255, 255, 0.9);
  border-bottom: solid 2px var(--gold1);
}

#header-container {
  color: var(--blue1);
  font-size: min(calc(10px + 2vw), 36px);
  height: 9vh;
  display: flex;
  align-items: center;
  justify-content: space-around;
  max-width: 1500px;
  margin: auto;
}
</style>
