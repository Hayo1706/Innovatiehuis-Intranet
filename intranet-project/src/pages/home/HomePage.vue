<template>
  <div class="container-fluid">
    <div class="row">
      <Warning v-if="this.warningIsVisible"></Warning>
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
import Warning from '../../shared_components/Warning.vue';
import Vue from 'vue';

export default {
  components: { AnnouncementWindow, ProjectsWindow, Warning },
  name: "HomePage",
  data: function () {
    return {
      announcementWindowKey: 0,
      warningIsVisible: false
    };
  },
  methods: {
    reloadAnnouncementWindow() {
      this.announcementWindowKey += 1;
    },
    triggerWarning() {
      this.warningIsVisible = true;
    }
  },
  created() {
    this.$emit('newHeaderTitle', 'Hoofdpagina');
    this.triggerWarning();

    var WarningClass = Vue.extend(Warning)
    var warning = new WarningClass();
    warning.$mount();
    this.$refs.alert_container.appendChild(warning.$el);

  }
};
</script>

<style>
</style>