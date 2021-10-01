<template>
<h2>Wie is een hond?</h2>
<button id=hayo_button @click="handleClick(true, 'hayo', $event)" :class="{ selected: selected_button == 'hayo' }">
  <span>Hayo</span>
</button>
<button id=pieter_button @click="handleClick(false, 'pieter', $event)" :class="{ selected: selected_button == 'pieter' }">
  <span>Pieter</span>
</button>
<button id=joppe_button @click="handleClick(true, 'joppe', $event)" :class="{ selected: selected_button == 'joppe_button' }">
  <span>Joppe</span>
</button>
<p v-show="showText">{{ this.message }}</p>
</template>

<script>
export default {
  name: 'App',
  data(){
    return {
      showText: false,
      message: '',
      toggle: false,
      selected_button: null,
      styleObject: {
        color: 'red'
      }
    }
  },
  methods: {
      handleClick(yes, name, event) {
        this.selected_button = event.target.id
        if (yes) this.message = 'Ja dat klopt.'
        else this.message = 'Nee dat is niet waar.'
        this.showText = true
        this.toggle = !this.toggle
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
  color: #1b1616;
  margin-top: 60px;
}
.selected {
  background-color: #41B883;
  color: red;
}
button {
  color: red;
  font-style: italic;
}
</style>
