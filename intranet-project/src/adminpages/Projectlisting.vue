<template>
  <div id="projectlisting">
    <span>{{ name }}</span>
    <span>{{ created }}</span>
    <span>{{ lastModified }}</span>
    <span>{{ parentProject }}</span>
    <span>{{ subprojectCount }}</span>

    <span>
      <img src="..\adminpages\images\people.png" />
      <img
        v-if="isArchived"
        src="https://cdn-icons-png.flaticon.com/512/60/60723.png"
      /><img
        v-else
        src="https://www.pngkey.com/png/full/876-8761970_download-button-comments-icon-png-archive-icon.png"
      />

      <img src="https://www.pngrepo.com/png/320601/512/crossed-pistols.png" />
    </span>
  </div>
</template>

<script>
export default {
  name: "Projectlisting",
  props: [
    "name",
    "created",
    "lastModified",
    "parentProject",
    "subprojectCount",
    "isArchived",
  ],
  data: function () {
    return {};
  },
  methods: {},
};
</script>

<style>
#projectlisting {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  color: black;
  flex-basis: 100%;
  gap: 60px;
}

span {
  flex: 1 1 0;
  width: 0;
  overflow-wrap: anywhere;
}
img {
  height: 5vh;
  padding-right: 20px;
}
</style>