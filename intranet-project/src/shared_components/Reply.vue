<template>
  <div>
    <div class="reply">
      <div v-if="this.editing">
        <textarea
          class="form-control"
          id="edit-text"
          style="height: 100px"
          v-model="this.editData.content"
        />
        <button @click="toggleEdit()">Annuleren</button>
        <button @click="saveEdits()">Opslaan</button>
      </div>
      <div v-else>
        <p>{{ this.content }}</p>
        <button @click="toggleEdit()">Wijzigen</button>
        <button @click="remove()">Verwijderen</button>
      </div>
    </div>
    <p style="text-align: right;">{{ this.username }} ({{ this.timestamp.toLocaleDateString() }})</p>
  </div>
</template>

<script>
import ProjectService from "@/services/ProjectService.js";

export default {
  name: "Reply",
  props: {
    id: { type: Number, required: true },
    announcementid: { type: Number, required: true },
    userid: { type: Number, required: true },
    username: { type: String, required: true },
    content: { type: String, required: true },
    timestamp: { type: Date, required: true }
  },
  data: function () {
    return {
      editData: { content: this.content + "" },
      editing: false
    };
  },
  methods: {
    toggleEdit() {
      this.editing = !this.editing;
    },
    saveEdits() {
      ProjectService.editReply(this.id, this.editData)
      .then((response) => {
        this.editing = false;
        this.reload();
        console.log(response);
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });

      this.$emit("reload");
    },
    remove() {
      ProjectService.deleteReply(this.id)
      .then((response) => {
        alert("Reactie is verwijderd!");
        // TODO: verwijder reactie uit scherm
        console.log(response);
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });

      this.$emit("reload");
    },
  },
};
</script>

<style scoped>
.reply {
  width: 100%;
  text-align: right;
  background-color: var(--gold3);
  border-style: inset;
  padding: 4px;
}
</style>