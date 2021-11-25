<template>
    <div>
      <FoldersView />
      <FilesView />
      <AnnouncementWindow />
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
    };
  },
 created(){
     this.$emit('loaded', 'Project: NAAM VAN PROJECT #' +  + this.$route.params.id)
 }
};
</script>

<style>

</style>