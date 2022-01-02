<template>
    <div class="component-container">
      <p>Personal Details</p>
    </div>
</template>

<script>
export default {
  name: "PersonalDetails",
  props: [

  ],
  data: function () {
    return {};
  },
}
</script>


<style scoped>
p {
  color: white;
  font-size: calc(2vw + 2vh);
  height: 100%;
  width: 500px;
  margin: 0;
  text-align: center;
  background-color: var(--blue4);
  border-style: outset;
  }
</style>