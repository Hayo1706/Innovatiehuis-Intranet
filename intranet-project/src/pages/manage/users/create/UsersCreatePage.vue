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
     this.$emit('newHeaderTitle', 'Nieuwe gebruiker toevoegen')
 }
};
</script>

<style>

</style>