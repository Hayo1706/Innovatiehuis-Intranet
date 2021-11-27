<template>
  <div id="announcementDiv">
    <h1 id="title">Announcement Window</h1>
    
    <div class="accordion" v-for="announcement in announcements" :key="announcement.id">
      <Announcement 
        v-bind:id="announcement.id" 
        v-bind:date="announcement.date" 
        v-bind:userid="announcement.userid" 
        v-bind:username="announcement.username" 
        v-bind:title="announcement.title" 
        v-bind:content="announcement.content" 
        v-on:reload="reload()"
        />
    </div>
  </div>
</template>

<script>
import Announcement from "./Announcement.vue"

export default {
  components: { Announcement },
  name: "AnnouncementWindow",
  props: [

  ],
  data: function () {
    return { announcements: [
      {id:5, date:new Date('December 17, 2021 13:24:00'), userid:1, username:"Niels Doornbos", title:"Politiebijeenkomst Kerst", content:"Hallo iedereen, vergeten jullie niet kerst met ons te vieren?\n\nGroeten de politie."},
      {id:4, date:new Date('December 07, 2021 15:14:00'), userid:1, username:"Niels Doornbos", title:"Sprintdemo #4", content:"Jongens ik heb aan jullie getwijfeld, maar wat een geweldige presentatie hebben jullie vandaag gegeven! Wij hebben er als team weer het volste vertrouwen in. Vooral de Batman-meme was een goede vondst!\n\nRecht zo die gaat,\nNiels."},
      {id:3, date:new Date('December 04, 2021 10:52:00'), userid:1, username:"Niels Doornbos", title:"Announcements verwijderen", content:"Hoe verwijder ik Announcements? Dat zou toch een feature zijn?"},
      {id:2, date:new Date('December 04, 2021 10:37:00'), userid:1, username:"Niels Doornbos", title:"Test", content:"Test test 123."},
      {id:1, date:new Date('December 04, 2021 10:37:00'), userid:69, username:"1337haxx0r", title:"Ik ben een hacker", content:"Haha mooi systeempje hoor jongens, lekker secure. :)"}
      ]};
  },
}
</script>


<style scoped>
#title {
  color: white;
  font-size: calc(1vw + 1vh);
  margin: 0;
  text-align: center;
  background-color: var(--blue4);
  border-style: outset;
  }
#announcementDiv {
  
}
</style>
