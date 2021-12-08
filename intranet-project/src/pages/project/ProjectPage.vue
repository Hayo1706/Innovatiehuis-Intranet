<template>
  <div>
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm">
          <div class="container-fluid">
            <div class="row">
              <div class="col-sm">
                <FoldersView />
              </div>
            </div>
            <div class="row">
              <div class="col-sm">
                <FilesView />
              </div>
            </div>
          </div>
        </div>
        <div class="col-sm">
          <AnnouncementWindow @reload="reloadAnnouncementWindow()" :key="this.announcementWindowKey">Mededelingen</AnnouncementWindow>/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilesView from './FilesView.vue';
import FoldersView from './FoldersView.vue';
import AnnouncementWindow from '../../shared_components/AnnouncementWindow.vue';

export default {
  components: { FilesView, FoldersView, AnnouncementWindow },
  name: "ProjectPage",
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
    this.$emit('newHeaderTitle', 'Project: NAAM VAN PROJECT #' + + this.$route.params.id)
  }
};
</script>

<style>
</style>