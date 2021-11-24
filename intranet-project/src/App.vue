<template>
    <div>
      <header>
        <p id="header_title_text">{{ header_title }}</p>
      </header>
      <router-view @loaded="setHeaderTitle"></router-view>
    </div>
</template>

<script>
export default {
  components: {},
  name: "App",
  data: function () {
    return {
      header_title: "",
    };
  },
  methods: {
    setHeaderTitle(header_title) {
      this.header_title = header_title;
      document.title = header_title;
    },
  },
};
</script>

<style>
header {
  width: 100%;
  height: 10vh;
  background-color: #28418a;
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
body {
  margin: 0;
}
</style>
