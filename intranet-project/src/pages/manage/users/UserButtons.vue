<template>
  <div>
    <ConfirmDialogue ref="confirmDialogue"></ConfirmDialogue>

    <div class="row" style="margin-right: 8px">
      <div class="col" title="Naar profiel" >
        <router-link :to="'/user/' + this.user.userid" title="Naar profiel">
          <div class="iconHolder">
            <img class="userIcon" src="@\assets\images\user.png" />
          </div>
        </router-link>
      </div>
      <div class="col" title="Mail sturen">
        <a :href="'mailto:' + user.email">
          <div class="iconHolder">
            <img src="@\assets\images\mail.png" />
          </div>
        </a>
      </div>
      <div class="col" title="Gebruiker bellen">
        <a :href="'tel:' + user.phone_number">
          <div class="iconHolder">
            <img src="@\assets\images\phone.png" />
          </div>
        </a>
      </div>
      <div class="col" title="Verwijder gebruiker">
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
  height: 2.5em;
  opacity: 40%;
  cursor: pointer;
}
img:hover {
  opacity: 55%;
}
.userIcon{
  opacity: 28%;
}
.userIcon:hover{
  opacity: 38%;
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