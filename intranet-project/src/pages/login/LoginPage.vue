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
          console.log(response.status, "User logged in successfully");

          //set to local storage: user id and user permission data retrieved from API
          for (var property in response.data[0]) {
            localStorage.setItem(property, response.data[0][property]);
          }
          localStorage.setItem("loggedIn", true);

          this.$router.push(this.redirectTarget);
        })
        .catch((err) => {
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
  },
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