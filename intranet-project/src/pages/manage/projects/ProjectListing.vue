<template>
  <div>
    <!-- for larger screens-->
    <div id="projectListing" class="container-fluid d-none d-lg-block">
      <div class="row">
        <div class="col">Popoplatform</div>
        <div class="col">11-11-2021</div>
        <div class="col">11-11-2021</div>
        <div class="col">Politieplatformen</div>
        <div class="col">5</div>
        <div class="col">
          <img src="@/assets/images/users_icon.png" /><img
            src="https://www.pngkey.com/png/full/876-8761970_download-button-comments-icon-png-archive-icon.png"
          />
          <img
            src="https://www.pngrepo.com/png/320601/512/crossed-pistols.png"
          />
        </div>
      </div>
      <hr />
    </div>

    <!-- for smaller screens-->
    <div id="projectListing" class="container-fluid d-sm-block d-lg-none">
      <div class="row">
        <VerticalHeader></VerticalHeader>
        <div class="col">
          <div>Popoplatform</div>
          <div>11-11-2021</div>
          <div>11-11-2021</div>
          <div><br />Politieplatformen</div>
          <div>5</div>
        </div>

        <div class="col">
          <img src="@/assets/images/users_icon.png" /><img
            src="https://www.pngkey.com/png/full/876-8761970_download-button-comments-icon-png-archive-icon.png"
          />
          <img
            src="https://www.pngrepo.com/png/320601/512/crossed-pistols.png"
          />
        </div>
      </div>
      <hr />
    </div>
  </div>
</template>

<script>
import VerticalHeader from "./VerticalHeader.vue";
export default {
  components: { VerticalHeader },
  name: "ProjectListing",
  data: function () {
    return {};
  },
  methods: {},
};
</script>

<style scoped>
#projectListing {
  font-family: AddeleThin;
}
.row {
  padding-top: 12px;
}
img {
  height: 5vh;
  padding-right: 20px;
  cursor: pointer;
}
</style>