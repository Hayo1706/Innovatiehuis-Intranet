<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-6">
        <PersonalDetails />
      </div>
      <div class="col-6">
        <ProjectsWindow />
      </div>
    </div>
  </div>
</template>

<script>
import PersonalDetails from './PersonalDetails.vue';
import ProjectsWindow from '../../shared_components/ProjectsWindow.vue';

export default {
  components: { PersonalDetails, ProjectsWindow },
  name: "UserPage",
  data: function () {
    return {
    };
  },
 created(){
    this.$emit('newHeaderTitle', 'Profiel: NAAM VAN USER #' + this.$route.params.id)
 }
};
</script>

<style>

</style>