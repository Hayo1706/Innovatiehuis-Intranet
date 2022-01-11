<template>
    <div>Pieter is een hond</div>
</template>

<script>
export default {
  components: {},
  name: "ProjectSettings",
  data: function () {
    return {
    };
  },
 created(){
     this.$emit('newHeaderTitle', 'HAAL PROJECTNAAM UIT API REQUEST: Instellingen')
 }
};
</script>

<style>

</style>