<template>
  <header>
    <p id="header_title_text">{{ header_title }}</p>
  </header>
</template>

<script>
export default {
  name: "AppHeader",
  props: ["header_title"],
  data: function () {
    return {};
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
</style>
