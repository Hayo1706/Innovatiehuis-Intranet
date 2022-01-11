<template>
  <div id="login" class="component-container">
    <div class="component-header"></div>
    <div style="text-align: center" class="component-body">
      <Label v-if="this.$route.query.resettoken === undefined">Oud wachtwoord:</Label>
      <br />
      <input
        v-model="this.old_password"
        v-if="this.$route.query.resettoken === undefined"
        style="text-align: center"
        type="password"
        v-on:keyup.enter="submit()"
      />
      <br />
      <Label>Nieuw wachtwoord:</Label>
      <br />
      <input
        v-model="this.new_password1"
        style="text-align: center"
        type="password"
        v-on:keyup.enter="submit()"
      />
      <br />
      <Label>Herhaal nieuw wachtwoord:</Label>
      <br />
      <input
        v-model="this.new_password2"
        style="text-align: center"
        type="password"
        v-on:keyup.enter="submit()"
      />
      <br />
      <br />
      <button class="full-button" style="margin: auto;" @click="submit()">Wijzig wachtwoord</button>
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
      old_password: "",
      new_password: "",
      redirectTarget: "/login",
    };
  },
  methods: {
    submit() {
      if (this.new_password1 == this.new_password2) {
        LoginService.changePassword(
          "old_password=" +
          this.old_password +
          "&new_password=" +
          this.new_password1,
          ((this.$route.query.resettoken !== undefined) ? this.$route.query.resettoken : '')
        )
          .then(() => {
            console.log("Password changed");
            this.$router.push(this.redirectTarget);
          }).catch((err) => {
            console.log(err);
            if (err.response) {
              console.log(err.response.status);
            }
          });
      } else {
        alert("De twee opgegeven nieuwe wachtwoorden komen niet overeen.")
      }
    },
  },
  created() {

    this.$emit("newHeaderTitle", "Wachtwoord wijzigen");
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