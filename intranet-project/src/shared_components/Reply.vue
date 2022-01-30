<template>
  <ConfirmDialogue ref="confirmDialogue"></ConfirmDialogue>
  <div class="reply">
    <strong>
      <router-link class="custom-link" :to="'/user/' + this.userid">{{ this.username }}</router-link>
    </strong>
    <strong
      style="color: rgba(0,0,0,0.5); margin-left: 1em;"
    >{{ this.timestamp.toLocaleDateString("nl-NL") }} {{ this.timestamp.toLocaleTimeString("nl-NL") }}</strong>
    <img
      v-if="canEditDelete()"
      @click="toggleEdit()"
      title="Aanpassen"
      class="component-header-button"
      src=".\..\assets\images\edit.png"
    />
    <img
      v-if="canEditDelete()"
      @click="remove()"
      title="Verwijderen"
      class="component-header-button"
      src=".\..\assets\images\delete.png"
    />

    <div>
      <div v-if="this.editing">
        <textarea
          oninput="this.style.height = ''; this.style.height = this.scrollHeight + 'px'"
          onclick="this.style.height = ''; this.style.height = this.scrollHeight + 'px'"
          class="form-control"
          id="edit-text"
          style="height: 100px"
          v-model="this.editData.content"
        />
        <button class="cancel-btn" @click="toggleEdit()">Annuleren</button>
        <button class="confirm-btn" @click="saveEdits()">Opslaan</button>
      </div>
      <div v-else>
        <p style="margin-bottom: 0px">{{ this.contentData }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import PermissionService from "@/services/PermissionService";
import ConfirmDialogue from "@/shared_components/ConfirmDialogue.vue";
import AlertService from "@/services/AlertService";
import AnnouncementService from "@/services/AnnouncementService";

export default {
  name: "Reply",
  loggedInUser: 0,
  components: { ConfirmDialogue },
  props: {
    id: { type: Number, required: true },
    announcementid: { type: Number, required: true },
    userid: { type: Number, required: true },
    username: { type: String, required: true },
    content: { type: String, required: true },
    timestamp: { type: Date, required: true },
  },
  data: function () {
    return {
      editData: { content: this.content + "" },
      editing: false,
      contentData: this.content
    };
  },
  async created() {
    this.loggedInUser = localStorage.getItem('userid')
  },
  methods: {
    toggleEdit() {
      this.editing = !this.editing;
    },
    canEditDelete() {
      return PermissionService.userHasPermission("may_update_any_reply") ||
        (PermissionService.userHasPermission("may_update_own_content") && this.loggedInUser == this.userid)
    },
    async saveEdits() {
      this.editing = false;
      AnnouncementService.editReply(this.id, this.editData)
        .then((response) => {
          this.contentData = this.editData.content;
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    async remove() {
      this.$emit("removeReply");
    },
  },
};
</script>

<style scoped>
.reply {
  border-radius: 1rem;
  padding: 1rem;
  background-color: white;
  margin: 10px 0px;
}

</style>