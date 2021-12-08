<template>
  <div>
    <AppHeader>{{ this.header_title }}</AppHeader>
    <router-view @newHeaderTitle="setHeaderTitle"></router-view>
  </div>
</template>

<script>
import AppHeader from "./shared_components/AppHeader.vue";
export default {
  components: { AppHeader },
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

