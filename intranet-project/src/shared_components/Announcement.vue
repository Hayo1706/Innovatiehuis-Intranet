<template>
  <div class="accordion-item">
    <h2 class="accordion-header" :id="'heading' + this.id">
      <div v-if="this.editing">
        <input v-model="this.editData.title" />
      </div>
      <div v-else>
        <button
          class="accordion-button"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="'#collapse' + this.id"
          aria-expanded="false"
          aria-controls="panelsStayOpen-collapseOne"
        >
          {{
            this.timestamp.toLocaleString("nl-NL", {
              day: "numeric",
              month: "long",
            })
          }}: {{ this.title }}
        </button>
      </div>
    </h2>
    <div
      :id="'collapse' + this.id"
      class="accordion-collapse collapse show"
      :aria-labelledby="'heading' + this.id"
    >
      <div class="accordion-body">
        <strong>
          <router-link :to="'/user/' + this.userid">
            {{ this.username }}
          </router-link>
        </strong>
        ({{ this.timestamp.toLocaleDateString("nl-NL") }})
        <br />

        <div v-if="this.editing">
          <textarea
            class="form-control"
            v-model="this.editData.content"
            style="height: 80px"
          />
          <button @click="toggleEdit()">Annuleren</button>
          <button @click="saveEdits()">Opslaan</button>
        </div>
        <div v-else>
          <p>{{ this.content }}</p>
          <button v-if="canEditDelete()" @click="remove()">Verwijderen</button>
          <button v-if="canEditDelete()" @click="toggleEdit()">Aanpassen</button>
          <button
            data-bs-toggle="modal"
            :data-bs-target="'#repliesModal' + this.id"
          >
            Reacties ({{ this.replies.length }})
          </button>
        </div>
      </div>
    </div>

    <ConfirmDialogue ref="confirmDialogue"></ConfirmDialogue>

    <div
      class="modal fade"
      :id="'repliesModal' + this.id"
      tabindex="-1"
      aria-labelledby="repliesModalLabel"
      aria-hidden="true"
    >
      <RepliesModal
        :key="this.repliesModalKey"
        :id="this.id"
        :title="this.title"
        :content="this.content"
        :timestamp="this.timestamp"
        :username="this.username"
        :userid="this.userid"
        :replies="this.replies"
        @reload="reload()"
      />
    </div>
  </div>
</template>

<script>
import AnnouncementService from "@/services/AnnouncementService.js";
import RepliesModal from "@/shared_components/RepliesModal.vue";
import PermissionService from "@/services/PermissionService";
import ConfirmDialogue from "@/shared_components/ConfirmDialogue.vue";

export default {
  name: "Announcement",
  components: { RepliesModal, ConfirmDialogue },
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
      repliesModalKey: { type: Number},
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
    canEditDelete(){
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
  background: linear-gradient(
    to left top,
    rgba(50, 50, 80, 0.5),
    rgba(225, 225, 225, 0.7)
  );
}
.accordion-button {
  background: var(--blue2);
  color: white;
}
.accordion-body {
}
</style>