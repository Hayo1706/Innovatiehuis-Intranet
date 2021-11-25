<template>
    <div />
</template>

<script>
export default {
  components: {},
  name: "UsersCreatePage",
  data: function () {
    return {
    };
  },
 created(){
     this.$emit('loaded', 'Nieuwe gebruiker toevoegen')
 }
};
</script>

<style>

</style>