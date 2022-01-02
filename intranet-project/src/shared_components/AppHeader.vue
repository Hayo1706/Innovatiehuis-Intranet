<template>
  <header>
      <p id="header_title_text">
        <img
          @click="logoClick()"
          src=".\..\assets\images\logo\square.png"
        />
        <slot></slot>
        <img
          @click="userClick()"
          src=".\..\assets\images\profile_icon.png"
        />
      </p>
  </header>
</template>

<script>
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
      this.$router.push("/user/1");
    },
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
#header_title_text {
  color: var(--blue1);
  font-size: calc(4vh);
  display: flex;
  justify-content: space-between;
  max-width: 1500px;
  margin: auto;
}
</style>
