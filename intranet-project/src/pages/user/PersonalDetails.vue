<template>
    <div class="component-container">
      <div class="row list">
        <div class="col-6">
          <div class="item">Naam: </div>
          <div class="item">Email: </div>
          <div class="item">Rol: </div>
          <div class="item">Aanmaakdatum: </div>
          <div class="item">Laatst gezien: </div>
          <div class="item">Wachtwoord: </div>
        </div>
        <div class="col-6">
          <div class="item">{{this.user.first_name}} {{this.user.last_name}}</div>
          <div class="item">{{this.user.email}}</div>
          <div class="item">{{this.user.role_name}}</div>
          <div class="item">{{this.created}}</div>
          <div class="item">{{(this.last_seen)}}</div>
          <div class="item"><router-link class="button"  to="/manage/resetpassword">Wachtwoord resetten</router-link></div>
        </div>
      </div>
    </div>
</template>

<script>
import UserService from "@/services/UserService";

export default {
  name: "PersonalDetails",
  components: {},
  props: [

  ],
  data: function () {
    return {
      user: "",
      created: "",
      last_seen: "",
    };
  },
  async created() {

    UserService.getUserById(1)
        .then((response) => {
          this.user = response[0];
          this.created = this.user.created.toLocaleString();
          this.last_seen = this.user.last_seen.toLocaleString();
          this.$emit('getUserEvent', this.user.first_name + " " + this.user.last_name);
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });

  },
}
</script>


<style scoped>
.list {
  color: var(--blue1);

  font-size: 20px
  }
.item{
  margin-bottom: 1vh;
  white-space: initial;
}
.button{
  font-size: 15px;
}
</style>