<template>
  <header>
    <p id="header_title_text">
      <img
        @click="logoClick()"
        src=".\..\assets\images\logo\square.png"
        style="position: absolute; left: 20px; height: 8vh;"
      />
      <slot></slot>
      <img
        @click="userClick()"
        src=".\..\assets\images\profile_icon.png"
        style="position: absolute; right: 20px; height: 8vh;"
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
  height: 5vh;
  padding-right: 20px;
  cursor: pointer;
}
header {
  width: 100%;
  height: 10vh;
  /*background-color: var(--blue1);*/
  background: linear-gradient(to right bottom, rgba(255,255,255,0.7), rgba(255,255,255,0.8));
  backdrop-filter: blur(4rem);
  border-bottom: solid 2px var(--gold1);
}
#header_title_text {
  color: var(--blue1);
  font-size: calc(2vw + 2vh);
  height: 100%;
  margin: 0;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
