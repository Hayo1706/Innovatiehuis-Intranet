<template>
  <div class="container-fluid">
    <div class="row">
      <div class= "col-8">
        <ProjectsWindow>Mijn Projecten</ProjectsWindow>
        <router-link to="/manage/users">Gebruikersoverzicht</router-link>
        <br>
        <router-link to="/manage/projects">Projectenoverzicht</router-link>
      </div>
      <div class= "col-4">
        <AnnouncementWindow>Algemene Mededelingen</AnnouncementWindow>
      </div>
    </div>
  </div>
</template>

<script>
import AnnouncementWindow from '../../shared_components/AnnouncementWindow.vue';
import ProjectsWindow from '../../shared_components/ProjectsWindow.vue';

export default {
  components: { AnnouncementWindow, ProjectsWindow },
  name: "HomePage",
  data: function () {
    return {
    };
  },
 created(){
     this.$emit('loaded', 'Hoofdpagina')
 }
};
</script>

<style>

</style>