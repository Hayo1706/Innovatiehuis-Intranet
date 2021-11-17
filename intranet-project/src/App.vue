<template>
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta http-equiv="X-UA-Compatible" content="IE=edge" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Intranet</title>
    </head>
    <body>
      <header>
        <p id="header_title_text">{{ header_title }}</p>
      </header>
      <allprojects></allprojects>
    </body>
  </html>
</template>

<script>
import Allprojects from "./adminpages/Allprojects.vue";
export default {
  components: { Allprojects },
  name: "App",
  data: function () {
    return {
      header_title: "Projecten - Overzicht",
    };
  },
  methods: {
    setHeaderTitle(header_title) {
      this.header_title = header_title;
    },
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@800&display=swap");
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
  font-family: "Montserrat", sans-serif;
}
body {
  margin: 0;
}
</style>
