<template>
    <div>
      <app-header>
        <p id="header_title_text">{{ header_title }}</p>
      </app-header>
    </div>
</template>

<script>
export default {
  name: "AppHeader",
  props: [

  ],
  data: function () {
    return {};
  },
  methods: {
    setHeaderTitle(header_title) {
      this.header_title = header_title;
      document.title = header_title;
    },
  },
}
</script>


<style scoped>
app-header {
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
