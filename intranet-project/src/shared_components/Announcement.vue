<template>
  <div class="accordion-item">
    <h2 class="accordion-header" :id="'heading' + this.id">
      <div v-if="this.editing">
        <input v-model="this.editData.title">
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
            this.timestamp.toLocaleString("nl-NL", { day: "numeric", month: "long" })
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
        <strong
          ><router-link :to="'/user/' + this.id">{{
            this.username
          }}</router-link></strong
        >
        ({{ this.timestamp.toLocaleDateString("nl-NL") }}) <br />

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
          <button @click="remove()">Verwijderen</button>
          <button @click="toggleEdit()">Aanpassen</button>
          <button data-bs-toggle="modal" :data-bs-target="'#repliesModal' + this.id">
            Reacties ({{ this.replies.length }})
          </button>
        </div>
      </div>
    </div>

    <div
      class="modal fade"
      :id="'repliesModal' + this.id"
      tabindex="-1"
      aria-labelledby="repliesModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog" ref="modal">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="repliesModalLabel">
              {{ this.title }}
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="announcement-in-modal">{{ this.content }}</div>
            <p>{{ this.username }} ({{ this.timestamp.toLocaleDateString("nl-NL") }})</p>


            <div v-for="reply in this.replies" :key="reply.replyid">
              <Reply
                :id="reply.replyid"
                :announcementid="reply.announcementid"
                :userid="reply.userid"
                :username="reply.firstname + ' ' + reply.lastname"
                :timestamp="reply.timestamp"
                :content="reply.content"
                v-on:reload="reload()"
              />
            </div>

            <form>
              <div class="mb-3">
                <label for="message-text" class="col-form-label">Laat een reactie achter:</label>
                <textarea
                class="form-control"
                id="message-text"
                style="height: 100px"
                v-model="this.newReply.content"
                />
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="addReply()">
            Plaats reactie
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ProjectService from "@/services/ProjectService.js";
import Reply from "@/shared_components/Reply.vue";

export default {
  name: "Announcement",
  components: { Reply },
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
      editData: { title: this.title + "", content: this.content + "" },
      editing: false,
      replies: [],
      newReply: { userid: 1, content: ""} //TODO: get userid dynamically from JWT/Session
    };
  },
  async created() {
    console.log("load replies for announcement " + this.id)
    ProjectService.getRepliesByAnnouncement(this.id)
      .then((response) => {
        this.replies = response;
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
    });
  },
  methods: {
    remove() {
      ProjectService.deleteAnnouncement(this.id);
      alert("Mededeling is verwijderd! Herlaad om het resultaat te zien.");
      this.$emit("reload");
    },
    toggleEdit() {
      this.editing = !this.editing;
    },
    saveEdits() {
      ProjectService.editAnnouncement(this.id, this.editData)
            .then((response) => {
        console.log(response);
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });

      this.editing = false;
      this.$emit("reload");
    },
    addReply() {
      ProjectService.addReply(this.id, this.newReply) // TODO: get userid dynamically from JWT/Session
      .then((response) => {
        console.log(response);
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });
    },
  },
};
</script>

<style scoped>
.accordion-button {
  background-color: var(--blue2);
  color: white;
}
.announcement-in-modal {
  background-color: var(--blue3);
  border-style: outset;
  padding: 4px;
}
</style>