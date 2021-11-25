<template>
    <div>
      <label>Raad het wachtwoord van Niels:</label><br>
      <input type="text" v-model="password" placeholder= "Het is niet 123"><br>
      <button @click="submitPassword(password)">Verzenden</button><br>
      <p v-if="this.enteredWrongPassword" id="error-message">Nee dat is fout.</p>
    </div>
</template>

<script>
export default {
  components: {  },
  name: "LoginPage",
  data: function () {
    return {
      enteredWrongPassword: false
    };
  },
  methods: {
    submitPassword(password) {
      if (password == "1234") this.$router.push("/home");
      else this.enteredWrongPassword = true;
    }
  },
 created(){
 }
};
</script>

<style>
#error-message {
  color: red;
}
</style>