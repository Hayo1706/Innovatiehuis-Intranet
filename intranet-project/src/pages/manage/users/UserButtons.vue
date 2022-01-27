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
        <div @click="handleDeleteUser()" v-show="canDelete()">
          <div class="iconHolder">
            <img src="@\assets\images\delete.png" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PermissionService from "@/services/PermissionService.js";
import ConfirmDialogue from "@/shared_components/ConfirmDialogue.vue";

export default {
  props: ["user"],
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
    }
  },
};
</script>
<style scoped>
.col {
  padding: 0 3px;
}
img {
  height: 3em;
  cursor: pointer;
  opacity: 60%;
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