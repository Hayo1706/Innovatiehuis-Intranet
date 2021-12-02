<template>
  <div id="announcement-window">
    <div id="title">
      <label>Mededelingen</label>
      <button id="add-button" data-bs-toggle="modal" data-bs-target="#announcementModal"></button>
    </div>

    <div class="accordion" v-for="announcement in this.announcements" :key="announcement.id">
      <Announcement 
        v-bind:id="announcement.announcementid" 
        v-bind:date="announcement.timestamp" 
        v-bind:userid="announcement.userid" 
        v-bind:username="announcement.firstname + ' ' + announcement.lastname" 
        v-bind:title="announcement.title" 
        v-bind:content="announcement.content" 
        v-on:reload="reload()"
        />
    </div>

<div class="modal fade" id="announcementModal" tabindex="-1" aria-labelledby="announcementModalLabel" aria-hidden="true">
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
            <input type="text" class="form-control" id="title-text" :value="this.newAnnouncement.title">
          </div>
          <div class="mb-3">
            <label for="message-text" class="col-form-label">Inhoud:</label>
            <textarea class="form-control" id="message-text" style="height: 400px" :value="this.newAnnouncement.content"></textarea>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuleren</button>
        <button type="button" class="btn btn-primary" @onclick="addAnnouncement()">Bevestigen</button>
      </div>
    </div>
  </div>
</div>

  </div>
</template>

<script>
import Announcement from "./Announcement.vue"
import { getAnnouncementsByProject } from "@/services/ProjectService.js"
import { postAnnouncement } from "@/services/ProjectService.js"

export default {
  components: { Announcement },
  name: "AnnouncementWindow",
  props: [

  ],
  data: function () {
    return { newAnnouncement: { title: "", content: "" },
      announcements: [],
      testAnnouncements: [
      {id:5, date:new Date('December 17, 2021 13:24:00'), userid:1, username:"Niels Doornbos", title:"Politiebijeenkomst Kerst", content:"Hallo iedereen, vergeten jullie niet kerst met ons te vieren?\n\nGroeten de politie."},
      {id:4, date:new Date('December 07, 2021 15:14:00'), userid:1, username:"Niels Doornbos", title:"Sprintdemo #4", content:"Jongens ik heb aan jullie getwijfeld, maar wat een geweldige presentatie hebben jullie vandaag gegeven! Wij hebben er als team weer het volste vertrouwen in. Vooral de Batman-meme was een goede vondst!\n\nRecht zo die gaat,\nNiels."},
      {id:3, date:new Date('December 04, 2021 10:52:00'), userid:1, username:"Niels Doornbos", title:"Announcements verwijderen", content:"Hoe verwijder ik Announcements? Dat zou toch een feature zijn?"},
      {id:2, date:new Date('December 04, 2021 10:37:00'), userid:1, username:"Niels Doornbos", title:"Test", content:"Test test 123."},
      {id:1, date:new Date('December 04, 2021 10:37:00'), userid:69, username:"1337haxx0r", title:"Ik ben een hacker", content:"Haha mooi systeempje hoor jongens, lekker secure. :)"}
      ]};
  },
  methods: {
    addAnnouncement() {
      postAnnouncement(10, this.newAnnouncement); //TODO: get project id dynamically
      this.newAnnouncement.title = "";
      this.newAnnouncement.content = "";
    }
  },
  async created() {
    getAnnouncementsByProject(10) //TODO: get project id dynamically
      .then((response) => {
        this.announcements = response;
        console.log(this.announcements);
      })
      .catch((err) => {
        console.log(err);
        if (!err.response) {
          alert("Network error! Connection timed out!");
        }
      });
  }
}
</script>


<style scoped>
#title {
  color: white;
  font-size: calc(1vw + 1vh);
  margin: 0;
  padding: 2px;
  padding-left: 10px;
  background-color: var(--blue1);
  border-style: outset;
  width: auto;
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
