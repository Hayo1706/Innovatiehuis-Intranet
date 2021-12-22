<template>
  <div id="login" class="component-container">
    <div class="component-header">Login</div>
    <div style="text-align: center" class="component-body">
      <input
        v-model="this.loginAttempt.email"
        style="text-align: center"
        type="text"
        placeholder="e-mail"
      /><br />
      <input
        v-model="this.loginAttempt.password"
        style="text-align: center"
        type="password"
        placeholder="wachtwoord"
      /><br />
      <button @click="submit()">Verzenden</button><br />
      <p v-if="this.enteredWrongPassword" id="error-message">
        Nee dat is fout.
      </p>
    </div>
  </div>
</template>

<script>
import LoginService from "../../services/LoginService";

export default {
  components: {},
  name: "LoginPage",
  data: function () {
    return {
      enteredWrongPassword: false,
      loginAttempt: { email: "", password: "" },
    };
  },
  methods: {
    submit() {
      LoginService.attemptLogin(this.loginAttempt)
        .then((response) => {
          console.log(response);
          this.$router.push("/home");
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
          this.enteredWrongPassword = true;
        });
    },
  },
  created() {
    this.$emit("newHeaderTitle", "Innovatiehuis Intranet");
  },
};
</script>

<style>
#login {
  width: 400px;
  margin: auto;
}
#center {
  margin: auto;
}
#error-message {
  color: red;
}
</style>