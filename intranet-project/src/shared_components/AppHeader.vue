<template>
  <header>
    <div class="float-left">
      <img @click="logoClick()" src=".\..\assets\images\logo\square.png" style="height: 8vh;" />
    </div>
    <p id="header_title_text">
      <slot></slot>
    </p>
    <div class="float-right">
      <img @click="userClick()" src=".\..\assets\images\profile_icon.png" style="height: 8vh;" />
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
    }
  },
};
</script>


<style scoped>
img {
  height: 5vh;
  padding-right: 20px;
  cursor: pointer;
}
header {
  width: 100%;
  height: 10vh;
  background-color: var(--blue1);
  -webkit-box-shadow: 3px 3px 1px 2p var(--gold1);
  box-shadow: 3px 3px 1px 2px var(--gold1);
}
#header_title_text {
  color: white;
  font-size: calc(2vw + 2vh);
  height: 100%;
  margin: 0;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: Montserrat;
}
</style>
