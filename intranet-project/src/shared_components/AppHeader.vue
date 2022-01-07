<template>
  <header v-if="this.$route.path !== '/login'">
    <div id="header_title_text">
      <img class="logo"
           @click="logoClick()"
           src=".\..\assets\images\logo\square.png"
      />
      <slot></slot>
      <div id="doubleimage">
        <img
            @click="userClick()"
            src=".\..\assets\images\profile_icon.png"
        />
        <img
            @click="logout()"
            src=".\..\assets\images\logout-icon.png"
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
      this.$router.push("/user/" + localStorage.getItem('userid'));
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
.logo{
  margin-left: 8vh;
}

#header_title_text {
  color: var(--blue1);
  font-size: min(calc(10px + 2vw), 36px);
  display: flex;
  justify-content: space-around;
  align-items: center;
  max-width: 1500px;
  margin: auto;
  height: 9vh;
}
#doubleimage{
  padding: 0;
  margin: 0;
  height: 100%;
  align-items: center;
  display: flex;

}
</style>
