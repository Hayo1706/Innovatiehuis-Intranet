<template>
    <p>Jullie zijn allemaal honden!</p>
</template>

<script>
export default {
  components: {},
  name: "Test",
  data: function () {
    return {
      header_title: "Projecten - Overzicht",
    };
  },
 created(){
     this.$emit('loaded', 'Test')
 }
};
</script>
<style>
p{
    font-size: 50px;
}
</style>