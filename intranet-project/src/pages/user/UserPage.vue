<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-6">

        <PersonalDetails @getUserEvent="(name) => {
          this.$emit('newHeaderTitle', name)
        }" />
      </div>
      <div class="col-sm-6">
        <ProjectsWindow>Gebruikers Projecten</ProjectsWindow>
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
};
</script>

<style>

</style>