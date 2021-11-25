<template>
    <div>
      <PersonalDetails />
      <ProjectsWindow />
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
    this.$emit('loaded', 'Profiel: NAAM VAN USER #' + this.$route.params.id)
 }
};
</script>

<style>

</style>