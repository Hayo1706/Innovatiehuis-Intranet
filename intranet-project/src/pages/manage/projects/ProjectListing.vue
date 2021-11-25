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
        <div class="col"></div>
      </div>
      <br />
    </div>

    <!-- for smaller screens-->
    <div id="projectListing" class="container-fluid d-small-block d-lg-none">
      <div class="row">
        <VerticalHeader></VerticalHeader>
        <div class="col">
          <div>Popoplatform</div>
          <div>11-11-2021</div>
          <div>11-11-2021</div>
          <div>Politieplatformen</div>
          <div>5</div>
          <br />
        </div>

        <div class="col"></div>
      </div>
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
</style>