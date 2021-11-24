<template>
    <div>
      <FoldersView />
      <FilesView />
      <ProjectsWindow />
    </div>
</template>

<script>
import FilesView from './FilesView.vue';
import FoldersView from './FoldersView.vue';
import ProjectsWindow from './../../shared_components/ProjectsWindow.vue';

export default {
  components: { FilesView, FoldersView, ProjectsWindow },
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