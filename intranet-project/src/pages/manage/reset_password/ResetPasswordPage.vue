<template>
   <div id="login" class="component-container">
    <div class="component-header"></div>
    <div style="text-align: center" class="component-body">
      <input
          v-model="this.old_password"
          style="text-align: center"
          type="password"
          placeholder="Oude wachtwoord"
          v-on:keyup.enter="submit()"
      />
      <input
        v-model="this.new_password"
        style="text-align: center"
        type="password"
        placeholder="Nieuwe wachtwoord"
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
      old_password: "",
      new_password: "",
      redirectTarget: "/login",
    };
  },
  methods: {
    submit() {
      LoginService.changePassword(
          "old_password=" +
          this.old_password +
          "&new_password=" +
          this.new_password
      )
      .then(() => {
        console.log("Password changed");
        this.$router.push(this.redirectTarget);
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