<template>
  <div class="user-listing">
    <div class="row">
      <VerticalHeader class="d-block d-lg-none"></VerticalHeader>
      <!-- small screens-->
      <div class="col d-block d-lg-none">
        <div class="userButton mobileRow" @click="onClick()">
          {{ user.firstname }}
        </div>
        <div class="mobileRow">
          {{
            user.createdat.toLocaleString("nl-NL", {
              day: "numeric",
              month: "numeric",
              year: "numeric",
              hour: "numeric",
              minute: "numeric",
              second: "numeric",
            })
          }}
        </div>
        <div class="mobileRow"></div>
        <div class="mobileRow"></div>
        <div class="mobileRow"></div>
        <div class="mobileRow"></div>
      </div>

      <!-- large screens-->
      <div class="col d-none d-lg-block" @click="onClick()">
        <div class="userButton">{{ user.firstname }}</div>
      </div>
      <div class="col d-none d-lg-block">
        {{
          user.createdat.toLocaleString("nl-NL", {
            day: "numeric",
            month: "numeric",
            year: "numeric",
            hour: "numeric",
            minute: "numeric",
            second: "numeric",
          })
        }}
      </div>
      <div class="col d-none d-lg-block"></div>
      <div class="col d-none d-lg-block"></div>
      <div class="col d-none d-lg-block"></div>
      <div class="col d-none d-lg-block"></div>

      <div class="col"></div>
    </div>
  </div>
</template>

<script>
import VerticalHeader from "./VerticalHeader.vue";
export default {
  props: ["user"],
  components: { VerticalHeader },
  name: "UserListing",
  data: function () {
    return {};
  },
  methods: {
    onClick() {
      this.$router.push("/user/" + this.user.userid);
    },
  },
};
</script>

<style scoped>
.user-listing {
  background-color: var(--blue3);
  margin: 3px;
  padding: 10px;
}
.row {
  padding-top: 12px;
}
.userButton {
  font-weight: bold;
  background-color: var(--gold2);
  color: var(--blue1);
  border-style: outset;
  border-radius: 8px;
  padding-left: 10px;
  padding-right: 10px;
  height: fit-content;
  margin-bottom: 10px;
  box-sizing: border-box;
  cursor: pointer;
  width: fit-content;
}
.mobileRow {
  height: 50px;
}
</style>