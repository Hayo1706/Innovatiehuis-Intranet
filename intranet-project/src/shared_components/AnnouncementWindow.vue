<template>
  <div class="component-container">
    <div class="component-header">
      <slot></slot>

      <img
        data-toggle="tooltip" data-placement="bottom" title="Mededeling toevoegen"
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
        :key="announcement"
      >
        <Announcement
          :id="announcement.announcementid"
          :timestamp="announcement.timestamp"
          :userid="announcement.userid"
          :username="announcement.first_name + ' ' + announcement.last_name"
          :title="announcement.title"
          :content="announcement.content"
          @reload="reload()"
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
                  <label for="message-text" class="col-form-label"
                    >Inhoud:</label
                  >
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
  </div>
</template>

<script>
import Announcement from "./Announcement.vue";
import { getPathArguments } from "@/services/DataConverter.js";
import AnnouncementService from "@/services/AnnouncementService.js";
import PermissionService from "@/services/PermissionService";
import AlertService from "@/services/AlertService";

export default {
  components: { Announcement },
  name: "AnnouncementWindow",
  props: [],
  data: function () {
    return {
      newAnnouncement: { title: "", content: "" },
      announcements: [],
      pathArgs: getPathArguments(this.$route.path),
    };
  },
  methods: {
    queryData() {
      AnnouncementService.getAnnouncementsByProject(this.pathArgs.project)
        .then((response) => {
          this.announcements = response;
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    canAddAnnouncement(){
      return PermissionService.userHasPermission("may_create_announcement_anywhere") ||
          (PermissionService.userHasPermission("may_create_announcement_in_own_project") && this.$route.path.indexOf('/project') > -1)
    },
    addAnnouncement() {
      AnnouncementService.postAnnouncement(
        this.pathArgs.project,
        this.newAnnouncement
      )
        .then((response) => {
          this.newAnnouncement.title = "";
          this.newAnnouncement.content = "";
          this.reload();
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    reload() {
      console.log("updating key");
      this.$emit("reload");
    },
  },
  async created() {
    this.queryData();
  },
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
