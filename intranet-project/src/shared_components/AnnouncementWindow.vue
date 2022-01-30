<template>
  <ConfirmDialogue ref="confirmDialogue"></ConfirmDialogue>
  <div class="component-container">
    <div class="component-header">
      <slot></slot>

      <img
        data-toggle="tooltip"
        data-placement="bottom"
        title="Mededeling toevoegen"
        class="component-header-button"
        src="./../assets/images/add_icon.png"
        data-bs-toggle="modal"
        data-bs-target="#announcementModal"
        v-if="canAddAnnouncement()"
      />
    </div>
    <div class="component-body">
      <div
        class="accordion"
        v-for="announcement in this.announcements"
        :key="announcement.announcementid"
      >
        <Announcement
          v-bind:id="announcement.announcementid"
          v-bind:timestamp="announcement.timestamp"
          v-bind:userid="announcement.userid"
          v-bind:username="announcement.first_name + ' ' + announcement.last_name"
          v-bind:title="announcement.title"
          v-bind:content="announcement.content"
          @removeAnnouncement="removeAnnouncement(announcement.announcementid)"
        />
      </div>
      <label v-if="this.announcements.length == 0">Er zijn nog geen mededelingen!</label>

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
              <h5 class="modal-title" id="announcementModalLabel">Nieuwe mededeling</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form>
                <div class="mb-3">
                  <label for="recipient-name" class="col-form-label">Titel:</label>
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
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuleren</button>
              <button
                type="button"
                :disabled="this.newAnnouncement.title == '' || this.newAnnouncement.content == ''"
                class="btn btn-primary"
                data-bs-dismiss="modal"
                @click="addAnnouncement()"
              >Bevestigen</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Announcement from "./Announcement.vue";
import { getPathArguments } from "@/services/DataConverter.js";
import AnnouncementService from "@/services/AnnouncementService.js";
import PermissionService from "@/services/PermissionService";
import AlertService from "@/services/AlertService";
import ConfirmDialogue from "@/shared_components/ConfirmDialogue.vue";

export default {
  components: { Announcement, ConfirmDialogue },
  name: "AnnouncementWindow",
  props: [],
  data: function () {
    return {
      newAnnouncement: { title: "", content: "" },
      announcements: [],
      pathArgs: getPathArguments(this.$route.path),
    };
  },
  async created() {
    this.queryData();
  },
  methods: {
    queryData() {
      AnnouncementService.getAnnouncementsByProject(this.pathArgs.project)
        .then((response) => {
          this.announcements = response.data.result;
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    canAddAnnouncement() {
      return PermissionService.userHasPermission("may_create_announcement_anywhere") ||
        (PermissionService.userHasPermission("may_create_announcement_in_own_project") && this.$route.path.indexOf('/project') > -1)
    },
    async addAnnouncement() {
      const ok = await this.$refs.confirmDialogue.show({
        title: "Mededeling plaatsen",
        message: (typeof this.pathArgs.project == 'undefined')
          ? 'Let op: iedereen met toegang tot de hoofdpagina kan deze mededeling zien! Wil je deze mededeling plaatsen?'
          : 'Wil je deze mededeling plaatsen?',
        okButton: "Plaats mededeling",
      });
      if (ok) {
        AnnouncementService.postAnnouncement(
          this.pathArgs.project,
          this.newAnnouncement
        )
          .then((response) => {
            this.renderNewAnnouncement();
            this.newAnnouncement.title = "";
            this.newAnnouncement.content = "";
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            AlertService.handleError(err);
          });
      }
    },
    async renderNewAnnouncement() {
      let new_id = 0;
      if (this.announcements.length > 0) {
        new_id = Math.max(...this.announcements.map((announcement) => { return announcement.announcementid })) + 1;
      }
      this.announcements.unshift({
        announcementid: new_id,
        timestamp: new Date(),
        userid: parseInt(localStorage.getItem("userid")),
        first_name: localStorage.getItem("first_name"),
        last_name: localStorage.getItem("last_name"),
        title: this.newAnnouncement.title,
        content: this.newAnnouncement.content
      })
      console.log("HENK")
      console.log(this.announcements);
    },
    async removeAnnouncement(announcementid) {
      const ok = await this.$refs.confirmDialogue.show({
        title: "Mededeling verwijderen",
        message: 'Wil je deze mededeling echt verwijderen?'
      });
      if (ok) {
        AnnouncementService.deleteAnnouncement(announcementid)
          .then((response) => {
            this.announcements = this.announcements.filter(function (announcement) {
              return announcement.announcementid !== announcementid;
            });
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            AlertService.handleError(err);
          });
      }
    }
  }
};
</script>


<style scoped>
#add-button {
  background-image: url("./../assets/images/add_icon.png");
}
.btn-secondary {
  background-color: var(--blue4);
}
.btn-primary {
  background-color: var(--blue1);
}
</style>
