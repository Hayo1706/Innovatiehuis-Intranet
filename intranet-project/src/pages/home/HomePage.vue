<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-6">
        <ProjectsWindow>Mijn Projecten</ProjectsWindow>
      </div>
      <div class="col-sm-6">
        <AnnouncementWindow
          @reload="reloadAnnouncementWindow()"
          :key="this.announcementWindowKey"
        >Algemene Mededelingen</AnnouncementWindow>
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
      announcementWindowKey: 0
    };
  },
  methods: {
    reloadAnnouncementWindow() {
      this.announcementWindowKey += 1;
    }
  },
  created() {
    this.$emit('newHeaderTitle', 'Welkom, ' + localStorage.getItem('first_name'));
  }
};
</script>

<style>

</style>