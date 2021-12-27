<template>
  <div class="container-fluid">
    <div class="row">
      <div class="alert alert-warning alert-dismissible fade show" role="alert">
        <strong>Holy guacamole!</strong> You should check in on some of those fields below.
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </div>
      <div class="col-8">
        <ProjectsWindow>Mijn Projecten</ProjectsWindow>
      </div>
      <div class="col-4">
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
    this.$emit('newHeaderTitle', 'Hoofdpagina');
  }
};
</script>

<style>
</style>