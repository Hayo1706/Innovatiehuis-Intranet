<template>
    <div />
</template>

<script>
export default {
  components: {},
  name: "ProjectMembersPage",
  data: function () {
    return {
    };
  },
 created(){
     this.$emit('loaded', 'HAAL PROJECTNAAM UIT API REQUEST: Projectleden')
 }
};
</script>

<style>

</style>