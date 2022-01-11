<template>
  <div class="modal-dialog" ref="modal">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="repliesModalLabel">{{ this.title }}</h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>
      <div class="modal-body">
        <div class="announcement-in-modal">
          <p>{{ this.content }}</p>
        </div>
        <p>
          {{ this.username }} ({{ this.timestamp.toLocaleDateString("nl-NL") }})
        </p>

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
          <div class="mb-3">
            <label for="message-text" class="col-form-label"
              >Laat een reactie achter:</label
            >
            <textarea
              class="form-control"
              id="message-text"
              style="height: 100px"
              v-model="this.newReply.content"
            />
          </div>
        </form>
      </div>
      <div v-if="canAddReply()" class="modal-footer">
        <button type="button" class="btn btn-primary" @click="addReply()">
          Plaats reactie
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import AnnouncementService from "@/services/AnnouncementService.js";
import Reply from "@/shared_components/Reply.vue";
import PermissionService from "@/services/PermissionService";

export default {
  name: "RepliesModal",
  components: { Reply },
  props: {
    replies: { type: Array, required: true },
    id: { type: Number, required: true },
    timestamp: { type: Date, required: true },
    userid: { type: Number, required: true },
    username: { type: String, required: true },
    title: { type: String, required: true },
    content: { type: String, required: true },
  },
  data: function () {
    return {
      newReply: { content: "" },
    };
  },
  async created() {},
  methods: {
    canAddReply(){
      return PermissionService.userHasPermission("may_create_reply_anywhere") ||
          PermissionService.userHasPermission("may_create_reply_in_own_project")

    },
    addReply() {
      console.log("current announcement id = " + this.id);
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
    },
    reload() {
      this.$emit("reload");
    },
  },
};
</script>

<style>
.announcement-in-modal {
  background-color: var(--blue3);
  border-style: outset;
  padding: 4px;
}
</style>