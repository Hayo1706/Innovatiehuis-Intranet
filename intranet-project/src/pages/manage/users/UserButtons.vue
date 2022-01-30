<template>
  <div>
    <ConfirmDialogue ref="confirmDialogue"></ConfirmDialogue>

    <div class="row" style="margin-right: 8px">
      <div class="col">
        <a :href="'mailto:' + user.email">
          <div class="iconHolder">
            <img src="@\assets\images\mail.png" />
          </div>
        </a>
      </div>
      <div class="col">
        <a :href="'tel:' + user.phone_number">
          <div class="iconHolder">
            <img src="@\assets\images\phone.png" />
          </div>
        </a>
      </div>
      <div class="col">
        <div @click="handleDeleteUser()" v-if="canDelete() && showRemove">
          <div class="iconHolder">
            <img src="@\assets\images\delete.png" />
          </div>
        </div>
        <div v-else>
          <img style="visibility: hidden" src="@\assets\images\delete.png" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PermissionService from "@/services/PermissionService.js";
import ConfirmDialogue from "@/shared_components/ConfirmDialogue.vue";

export default {
  props: ["user", "showRemove"],
  components: { ConfirmDialogue },
  name: "UserButtons",
  data: function () {
    return {};
  },
  methods: {
    canDelete() {
      return PermissionService.userHasPermission("may_delete_any_user");
    },
    async handleDeleteUser() {
      this.$emit("removeUser", this.user.userid);
    },
  },
};
</script>
<style scoped>
.col {
  padding: 0 3px;
  float: left;
}
img {
  height: 3em;
  opacity: 60%;
  cursor: pointer;
}
img:hover {
  opacity: 80%;
}
.rotate {
  transform: rotate(180deg);
}
.link {
  text-decoration: none;
}
.icon-holder {
  display: inline-block;
}
</style>