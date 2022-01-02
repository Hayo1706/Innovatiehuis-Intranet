<template>
  <header>
    <div v-if="this.$route.path != '/login'">
      <img @click="logoClick()" src=".\..\assets\images\logo\square.png" />
    </div>
    <p id="header_title_text">
      <slot></slot>
    </p>
    <div v-if="this.$route.path != '/login'">
      <img @click="userClick()" src=".\..\assets\images\profile_icon.png" />
      <img @click="logout()" src=".\..\assets\images\logout-icon.png" style="height: 8vh;" />
    </div>
  </header>
</template>

<script>
import LoginService from "../services/LoginService";

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
    userClick() {
      this.$router.push("/user/1"); //TODO: dynamic
    },
    logout() {
      LoginService.logout();
      this.$router.push("/login");
    }
  },
};
</script>


<style scoped>
img {
  height: 8vh;
  padding: 5px;
  cursor: pointer;
}
header {
  width: 100%;
  height: 8vh;
  margin-top: 1vh;
  /*background-color: var(--blue1);*/
  background: linear-gradient(
    to bottom right,
    rgba(255, 255, 255, 0.8),
    rgba(225, 225, 225, 0.9)
  );
  backdrop-filter: blur(1rem);
  border-bottom: solid 2px var(--gold1);
  display: flex;
  justify-content: space-between;
}
#header_title_text {
  color: var(--blue1);
  font-size: calc(4vh);
  max-width: 1500px;
  margin: auto;
}
</style>
