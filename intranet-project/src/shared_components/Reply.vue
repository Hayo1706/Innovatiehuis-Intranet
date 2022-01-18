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
        <button @click="toggleEdit()">Annuleren</button>
        <button @click="saveEdits()">Opslaan</button>
      </div>
      <div v-else>
        <p style="margin-bottom: 0px">{{ this.content }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import AnnouncementService from "@/services/AnnouncementService.js";
import PermissionService from "@/services/PermissionService";
import ConfirmDialogue from "@/shared_components/ConfirmDialogue.vue";

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
      const ok = await this.$refs.confirmDialogue.show({
        title: "Reactie aanpassen",
        message: 'Wil je deze reactie echt aanpassen?'
      });
      if (ok) {
        this.editing = false;
        AnnouncementService.editReply(this.id, this.editData)
          .then((response) => {
            console.log("API RESPONDS: " + JSON.stringify(response));
            this.$emit("reload");
          })
          .catch((err) => {
            if (err.response) {
              console.log(err.response.status);
            }
          });
      }
    },
    async remove() {
      const ok = await this.$refs.confirmDialogue.show({
        title: "Reactie verwijderen",
        message: 'Wil je deze reactie echt verwijderen?'
      });
      if (ok) {
        AnnouncementService.deleteReply(this.id)
          .then((response) => {
            alert("Reactie is verwijderd!");
            console.log("API RESPONDS: " + JSON.stringify(response));
            this.$emit("reload"); // TODO: verwijder reactie uit scherm
          })
          .catch((err) => {
            if (err.response) {
              console.log(err.response.status);
            }
          });
      }
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