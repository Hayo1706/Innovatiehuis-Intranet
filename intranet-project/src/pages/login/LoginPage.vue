<template>
  <div id="login" class="component-container">
    <div class="component-header">
      <img src=".\..\..\assets\images\logo\square.png">
      <h2>Innovatiehuis Politie</h2>
    </div>
    <div style="text-align: center" class="component-body">
      <input
        v-model="this.loginAttempt.email"
        class="login-input"
        type="text"
        placeholder="e-mail"
        v-on:keyup.enter="submit()"
      />
      <br />
      <input
        v-model="this.loginAttempt.password"
        class="login-input"
        type="password"
        placeholder="wachtwoord"
        v-on:keyup.enter="submit()"
      />
            <input
        v-model="this.loginAttempt.authenticator_code"
        class="login-input"
        type="password"
        placeholder="authenticator code"
        v-on:keyup.enter="submit()"
      />
      <br />
      <div class="full-button" @click="submit()">
        Login
      </div>
    </div>
  </div>
</template>

<script>
import LoginService from "../../services/LoginService";
import AlertService from "../../services/AlertService";

export default {
  components: {},
  name: "LoginPage",
  data: function () {
    return {
      loginAttempt: { email: "", password: "", authenticator_code:"" },
      redirectTarget: "/home"
    };
  },
  methods: {
    submit() {
      LoginService.attemptLogin(
        "username=" +
        this.loginAttempt.email +
        "&password=" +
        this.loginAttempt.password+
                "&authenticator_code=" +
        this.loginAttempt.authenticator_code
      )
        .then((response) => {
          console.log(response.status, "User logged in successfully");

          //set to local storage: user id and user permission data retrieved from API
          for (var property in response.data.result[0]) {
            localStorage.setItem(property, response.data.result[0][property]);
          }
          localStorage.setItem("loggedIn", true);

          this.$router.push(this.redirectTarget);
        })
        .catch((err) => {
          console.log("HENK");
          AlertService.handleError(err);
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
    if (localStorage.getItem("userWasRedirected")) {
      console.log("User was logged out due to invalid or expired JSON Web Token.");
      AlertService.alert("Uw sessie is verlopen of ongeldig. Log in om terug te keren naar de vorige pagina.", "warning");
      localStorage.removeItem("userWasRedirected");
    }
  },
  mounted() {
    
  }
};
</script>

<style>
#login {
  width: 400px;
  margin: 22vh auto auto;
}
#login #center {
  margin: auto;
}
#login #error-message {
  color: red;
}
.login-input {
  text-align: center;
  min-width: 90%;
  height: fit-content;
  font-size: 14pt;
  margin: 4px;
}
#login .full-button{
  justify-content: center;
  width: 96%;
  margin: 16px auto 1px auto;
}
#login input{
  border:2px solid var(--blue4);
  border-radius: 0.5vh;
}
#login input:focus{
  outline: none !important;
  border:2px solid var(--blue2);
}
#login .component-header{
  display: flex;
  height: 2.5em;
  align-items: baseline;
}
#login .component-header img{
  height: 2em;
}
#login h2 {
  display: inline-block;
  font-family: AddeleThin;
  width: 100%;
  text-align: center;
}
#login .component-container{
  padding-bottom: 19px;
}
#login .component-body{
  padding-top: 14px;
}
</style>