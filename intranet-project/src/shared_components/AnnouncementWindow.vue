<template>
  <div id="announcement-window">
    <div id="title-bar">
      <label>Mededelingen</label>
      <button
        id="add-button"
        data-bs-toggle="modal"
        data-bs-target="#announcementModal"
      ></button>
    </div>

    <div
      class="accordion"
      v-for="announcement in this.announcements"
      :key="announcement.id"
    >
      <Announcement
        :id="announcement.announcementid"
        :timestamp="announcement.timestamp"
        :userid="announcement.userid"
        :username="announcement.firstname + ' ' + announcement.lastname"
        :title="announcement.title"
        :content="announcement.content"
        v-on:reload="reload()"
      />
    </div>

    <div
      class="modal fade"
      id="announcementModal"
      tabindex="-1"
      aria-labelledby="announcementModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="announcementModalLabel">
              Nieuwe mededeling
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="recipient-name" class="col-form-label"
                  >Titel:</label
                >
                <input
                  type="text"
                  class="form-control"
                  id="title-text"
                  v-model="this.newAnnouncement.title"
                />
              </div>
              <div class="mb-3">
                <label for="message-text" class="col-form-label">Inhoud:</label>
                <textarea
                  class="form-control"
                  id="message-text"
                  style="height: 400px"
                  v-model="this.newAnnouncement.content"
                ></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Annuleren
            </button>
            <button
              type="button"
              class="btn btn-primary"
              data-bs-dismiss="modal"
              @click="addAnnouncement()"
            >
              Bevestigen
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Announcement from "./Announcement.vue"
import { getPathArguments } from "@/services/DataConverter.js"
import ProjectService from "@/services/ProjectService.js";

export default {
  components: { Announcement },
  name: "AnnouncementWindow",
  props: [],
  data: function () {
    return {
      newAnnouncement: { title: "", content: "" },
      announcements: [],
      pathArgs: getPathArguments(this.$route.path)
      };
  },
  methods: {
    addAnnouncement() {
      ProjectService.postAnnouncement(this.pathArgs.project, this.newAnnouncement)
      .then((response) => {
        console.log(response);
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });

      this.newAnnouncement.title = "";
      this.newAnnouncement.content = "";
      this.reload();
    },
  },
  async created() {
    ProjectService.getAnnouncementsByProject(this.pathArgs.project)
      .then((response) => {
        this.announcements = response;
        console.log(this.announcements);
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });
  },
};
</script>


<style scoped>
#title-bar {
  color: white;
  font-size: calc(1vw + 1vh);
  margin: 0;
  padding-left: 10px;
  background-color: var(--blue1);
  border-style: outset;
  overflow: hidden;
  position: relative;
  width: 100%;
}

#announcement-window {
  overflow: auto;
  height: 90vh;
}
#add-button {
  height: 44px;
  width: 44px;
  background-image: url("./../assets/images/plus.png");
  background-size: cover;
  float: right;
}
.btn-secondary {
  background-color: var(--blue4);
}
.btn-primary {
  background-color: var(--blue1);
}
</style>
