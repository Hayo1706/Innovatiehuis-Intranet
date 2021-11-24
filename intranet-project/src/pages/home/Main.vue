<template>
    <div>
      <ProjectsWindow />
      <AnnouncementWindow />
      <router-link to="/manage/users" id="golden button">Gebruikersoverzicht</router-link>
      <br>
      <router-link to="/manage/projects" id="golden button">Projectenoverzicht</router-link>
    </div>
</template>

<script>
import AnnouncementWindow from './../../shared_components/AnnouncementWindow.vue';
import ProjectsWindow from './../../shared_components/ProjectsWindow.vue';

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