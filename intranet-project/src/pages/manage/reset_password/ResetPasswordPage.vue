<template>
   <div id="login" class="component-container">
    <div class="component-header"></div>
    <div style="text-align: center" class="component-body">

      <input
        v-model="this.password"
        style="text-align: center"
        type="password"
        placeholder="wachtwoord"
        v-on:keyup.enter="submit()"
      />
      <br/>
          <button @click="submit()">Verzenden</button>
      
    </div>
  </div>
</template>

<script>
import LoginService from "../../../services/LoginService";

export default {
  components: {},
  name: "ResetPasswordPage",
  data: function () {
    return {
      password: "",
    
    };
  },
  methods: {
    submit() {
      LoginService.attemptLogin(
        "&password=" +
        this.password
      )
        .then(() => {
 
        })
        .catch((err) => {
          console.log(err);
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
  },
  created() {

    this.$emit("newHeaderTitle", "Wachtwoord herstellen");
  },
};
</script>

<style>
#resetPassword {
  width: 400px;
  margin: 5vh auto auto;
}
#center {
  margin: auto;
}

</style>