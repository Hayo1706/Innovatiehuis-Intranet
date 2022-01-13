<template>
  <div id="login" class="component-container">
    <div class="component-header">Login</div>
    <div style="text-align: center" class="component-body">
      <input
        v-model="this.loginAttempt.email"
        style="text-align: center; width: 100%;"
        type="text"
        placeholder="e-mail"
        v-on:keyup.enter="submit()"
      />
      <br />
      <input
        v-model="this.loginAttempt.password"
        style="text-align: center; width: 100%;"
        type="password"
        placeholder="wachtwoord"
        v-on:keyup.enter="submit()"
      />
      <br />
      <div style="text-align: center;">
        <div class="full-button" @click="submit()">Aanmelden</div>
      </div>
      <br />
      <p
        v-if="this.redirectTarget != '/home' && !this.enteredWrongPassword"
        id="error-message"
      >
        Sessie is ongeldig of verlopen. Log in om terug te keren naar de vorige
        pagina.
      </p>
      <p id="error-message">{{ this.error }}</p>
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
      loginAttempt: { email: "", password: "" },
      redirectTarget: "/home",
      error: "",
      enteredWrongPassword: false,
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
          console.log(response.status);

          //set user id and user permission data retrieved from API
          for (var property in response.data[0]) {
            localStorage.setItem(property, response.data[0][property]);
          }
          localStorage.setItem("loggedIn", true);

          this.$router.push(this.redirectTarget);
        })
        .catch((err) => {
          console.log(err);
          if (err.response) {
            console.log(err.response.status);
          }
          this.error = err.response.data.response.message;
          console.log(this.err.response.data.response.message);
          this.enteredWrongPassword = true;
        });
    },
  },
  created() {
    if (localStorage.getItem("loggedIn")) {
      this.$router.push("/home");
      return;
    }
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
  margin: 5vh auto auto;
}
#center {
  margin: auto;
}
#error-message {
  color: red;
}
</style>