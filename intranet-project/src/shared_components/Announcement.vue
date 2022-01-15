<template>
  <ConfirmDialogue ref="confirmDialogue"></ConfirmDialogue>
  <div class="card" style="width: 100%;">
    <div class="card-body">
      <h5 class="card-title">
        <div v-if="this.editing">
          <input v-model="this.editData.title" />
        </div>
        <div v-else>
          {{ this.title }}
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
        </div>
      </h5>
      <div class="card-text">
        <strong>
          <router-link class="custom-link" :to="'/user/' + this.userid">{{ this.username }}</router-link>
        </strong>
        <strong style="color: rgba(0,0,0,0.5); margin-left: 1em;">
          {{ this.timestamp.toLocaleDateString("nl-NL")}} {{ this.timestamp.toLocaleTimeString("nl-NL")}}
        </strong>
        <br />
        <div v-if="this.editing">
          <textarea 
            oninput='this.style.height = ""; this.style.height = this.scrollHeight + "px"'
            onclick='this.style.height = ""; this.style.height = this.scrollHeight + "px"'
            class="form-control" 
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
  </div>

  <div class="accordion-item">
    <h2 class="accordion-header" :id="'heading' + this.id">
      <button
        class="accordion-button"
        type="button"
        data-bs-toggle="collapse"
        :data-bs-target="'#collapse' + this.id"
        aria-expanded="false"
        aria-controls="panelsStayOpen-collapseOne"
      >Reacties ({{ this.replies.length }})</button>
    </h2>
    <div
      :id="'collapse' + this.id"
      class="accordion-collapse collapse hide"
      :aria-labelledby="'heading' + this.id"
    >
      <div class="accordion-body">
        <div v-for="reply in this.replies" :key="reply">
          <Reply
            :id="reply.replyid"
            :announcementid="reply.announcementid"
            :userid="reply.userid"
            :username="reply.first_name + ' ' + reply.last_name"
            :timestamp="reply.timestamp"
            :content="reply.content"
            @reload="reload()"
          />
        </div>
        <form v-if="canAddReply()">
          <textarea
            class="form-control"
            id="message-text"
            placeholder="Laat een reactie achter..."
            v-model="this.newReply.content"
          />
          <div type="button" class="full-button" style="width: fit-content;" @click="addReply()">
            Plaats reactie
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import AnnouncementService from "@/services/AnnouncementService.js";
import PermissionService from "@/services/PermissionService";
import ConfirmDialogue from "@/shared_components/ConfirmDialogue.vue";
import Reply from "./Reply.vue";

export default {
  name: "Announcement",
  components: { ConfirmDialogue, Reply },
  loggedInUser: 0,
  props: {
    id: { type: Number, required: true },
    timestamp: { type: Date, required: true },
    userid: { type: Number, required: true },
    username: { type: String, required: true },
    title: { type: String, required: true },
    content: { type: String, required: true },
  },
  data: function () {
    return {
      repliesModalKey: { type: Number },
      editData: { title: this.title + "", content: this.content + "" },
      editing: false,
      replies: [],
      newReply: { content: "" },
    };
  },
  async created() {
    this.loggedInUser = localStorage.getItem('userid')
    AnnouncementService.getRepliesByAnnouncement(this.id)
      .then((response) => {
        this.replies = response;
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
      });
  },
  methods: {
    async remove() {
      const ok = await this.$refs.confirmDialogue.show({
        title: "Mededeling verwijderen",
        message: 'Wil je deze mededeling echt verwijderen?'
      });
      if (ok) {
        AnnouncementService.deleteAnnouncement(this.id);
        alert("Mededeling is verwijderd!");
        this.$emit("reload");
      }
    },
    canEditDelete() {
      return PermissionService.userHasPermission("may_update_any_announcement") ||
        (PermissionService.userHasPermission("may_update_own_content") && this.loggedInUser == this.userid)
    },
    toggleEdit() {
      this.editing = !this.editing;
    },
    async saveEdits() {
      const ok = await this.$refs.confirmDialogue.show({
        title: "Wijziging opslaan",
        message: 'Wil je deze wijziging echt opslaan?'
      });
      if (ok) {
        AnnouncementService.editAnnouncement(this.id, this.editData)
          .then((response) => {
            console.log(response);
            this.editing = false;
            this.editData.title = "";
            this.editData.content = "";
            this.$emit("reload");
          })
          .catch((err) => {
            if (err.response) {
              console.log(err.response.status);
            }
          });
      }
    },
    canAddReply(){
      return PermissionService.userHasPermission("may_create_reply_anywhere") ||
          PermissionService.userHasPermission("may_create_reply_in_own_project")

    },
    async addReply() {
      const ok = await this.$refs.confirmDialogue.show({
        title: "Reactie plaatsen",
        message: 'Wil je deze reactie echt plaatsen?',
        okButton: "Plaats reactie",
      });
      if (ok) {
        AnnouncementService.addReply(this.id, this.newReply)
          .then((response) => {
            console.log(response);
            this.newReply.content = "";
            this.$emit("reload");
          })
          .catch((err) => {
            if (err.response) {
              console.log(err.response.status);
            }
          });
      }
    },
    reload() {
      console.log("reloaded component RepliesModal");
      this.repliesModalKey += 1;
    },
  },
};
</script>

<style scoped>
.accordion-item {
  margin-bottom: 1vh;
}

.accordion-header {
  border-radius: 0px 0px 10px 10px;
}
.accordion-button {
  background: var(--blue2);
  color: white;
  border-radius: 0px 0px 10px 10px;
}
.accordion-body {
  border-radius: 0px 0px 10px 10px;
}

.accordion-item {
  border-radius: 0px 0px 10px 10px;
  background-color: rgba(180,180,180,0.3);
}

.card {
  border-radius: 10px 10px 0px 0px;
  background-color: rgba(255, 255, 255, 0.7);
}
</style>