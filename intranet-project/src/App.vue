<template>
<h2>Wie is een hond?</h2>
<button>
  <span @click="handeClick(true)">Hayo</span>
</button>
<button>
  <span @click="handeClick(false)">Pieter</span>
</button>
<button>
  <span @click="handeClick(true)">Joppe</span>
</button>
<p v-show="showText">{{ this.message }}</p>
</template>

<script>
export default {
  name: 'App',
  data(){
    return {
      showText: false,
      message: ""
    }
  },
  methods: {
      handeClick(yes) {
        if (yes) this.message = "Ja dat klopt."
        else this.message = "Nee dat is niet waar."
        this.showText = true
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
