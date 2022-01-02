<template>
  <header>
      <div id="header_title_text">
        <img class="logo"
          @click="logoClick()"
          src=".\..\assets\images\logo\square.png"
        />
        <slot></slot>
        <div>
        <img
          @click="userClick()"
          src=".\..\assets\images\profile_icon.png"
        />
        <img
          @click="logout()"
          src=".\..\assets\images\logout-icon.png"
          style="height: 8vh;"
        />
        </div>
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
  height: 8vh;
  padding: 5px;
  cursor: pointer;
}
header {
  width: 100%;
  height: 8vh;
  margin-top: 2vh;
  /*background-color: var(--blue1);*/
  background: linear-gradient(to bottom right, rgba(255,255,255,0.8), rgba(225,225,225,0.9));
  backdrop-filter: blur(1rem);
  border-bottom: solid 2px var(--gold1);
}
.logo{
  margin-left: 8vh;
}

#header_title_text {
  color: var(--blue1);
  font-size: calc(4vh);
  display: flex;
  justify-content: space-around;
  max-width: 1500px;
  margin: auto;
}
</style>
