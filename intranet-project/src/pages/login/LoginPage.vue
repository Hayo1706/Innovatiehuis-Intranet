<template>
  <div id="login" class="component-container">
    <div class="component-header">Login</div>
    <div style="text-align: center" class="component-body">
      <input
        v-model="this.loginAttempt.email"
        style="text-align: center"
        type="text"
        placeholder="e-mail"
        v-on:keyup.enter="submit()"
      /><br />
      <input
        v-model="this.loginAttempt.password"
        style="text-align: center"
        type="password"
        placeholder="wachtwoord"
        v-on:keyup.enter="submit()"
      /><br />
      <button @click="submit()">Verzenden</button><br />
      <p v-if="this.enteredWrongPassword" id="error-message">
        Gebruikersnaam en/of wachtwoord is incorrect.
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
      redirectTarget: "/home"
    };
  },
  methods: {
    submit() {
      LoginService.attemptLogin(
        "username=" +
          this.loginAttempt.email +
          "&password=" +
          this.loginAttempt.password
      )
        .then((response) => {
          console.log(response);

          localStorage.setItem("loggedIn", true);

          this.$router.push(this.redirectTarget);
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
    const previousRoute = localStorage.getItem("previousRoute");
    if (previousRoute) {
      this.redirectTarget = previousRoute;
    }
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