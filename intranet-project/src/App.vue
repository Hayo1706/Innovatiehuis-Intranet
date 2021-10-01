<template>
<button>
  <span @click="handeClick">hoi</span>
</button>
<h2 v-show="showText">Pieter is een hond</h2>
</template>

<script>
export default {
  name: 'App',
  data(){
    return {
      showText: false
    }
  },
  methods: {
      handeClick() {
        this.showText = !this.showText
      }
  }
  
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
