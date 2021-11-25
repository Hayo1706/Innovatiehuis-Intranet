<template>
  <div class="col">
    <img src="@/assets/images/users_icon.png" />
    <img
      v-if="project.isArchived"
      src="https://cdn-icons-png.flaticon.com/512/60/60723.png"
    />
    <img
      v-else
      src="https://www.pngkey.com/png/full/876-8761970_download-button-comments-icon-png-archive-icon.png"
    />
    <img src="https://www.pngrepo.com/png/320601/512/crossed-pistols.png" />
  </div>
</template>

<script>
export default {
  props: ["project"],
  components: {},
  name: "ProjectButtons",
  data: function () {
    return {};
  },
  methods: {},
};
</script>
<style scoped>
img {
  height: 5vh;
  padding-right: 20px;
  cursor: pointer;
}
</style>