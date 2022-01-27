<template>
  <div class="component-container">
    
      <div class="component-header">Persoonsgegevens</div>
        <div class="component-body">
          <div class="row list">
        <div class="d-block d-lg-none">
          <div>Naam:</div>
          <div class="item-text">{{ this.user.first_name }} {{ this.user.last_name }}</div>
          <div>Email:</div>
          <div class="item-text">{{ this.user.email }}</div>
          <div>Telefoonnummer:</div>
          <div class="item-text">{{ this.user.phone_number }}</div>
          <div>Rol:</div>
          <div class="item-text">{{ this.user.role_name }}</div>
          <div>Geregistreerd:</div>
          <div class="item-text">{{ this.created }}</div>
          <div>Laatst gezien:</div>
          <div class="item-text">{{ this.last_seen }}</div>
          <div
            v-if="show_password"
            class="full-button"
            @click="toResetPassword()"
          >Wachtwoord wijzigen</div>
        </div>
        <div class="col-6 d-none d-lg-block">
          <div class="item">Naam:</div>
          <div class="item">Email:</div>
          <div class="item">Telefoonnummer:</div>
          <div class="item">Rol:</div>
          <div class="item">Geregistreerd:</div>
          <div class="item">Laatst gezien:</div>
        </div>
        <div class="col-6 d-none d-lg-block">
          <div class="item-text">{{ this.user.first_name }} {{ this.user.last_name }}</div>
          <div class="item-text"><a :href="'mailto:' + this.user.email">{{ this.user.email }}</a></div>
          <div class="item-text"><a :href="'tel:' + this.user.phone_number">{{ this.user.phone_number }}</a></div>
          <div class="item-text">{{ this.user.role_name }}</div>
          <div class="item-text">{{ this.created }}</div>
          <div class="item-text">{{ this.last_seen }}</div>
          <div class="item-text"></div>
        </div>
      </div>
      <div class="button-wrapper">
        <div
          v-if="show_password"
          class="full-button"
          @click="toResetPassword()"
        >Wachtwoord wijzigen</div>
      </div>
    </div>
  </div>
</template>

<script>
import UserService from "@/services/UserService";
import AlertService from "../../services/AlertService";

export default {
  name: "PersonalDetails",
  components: {},
  props: [],
  data: function () {
    return {
      user: "",
      created: "",
      last_seen: "",
      show_password: false,
    };
  },
  async created() {
    this.getUser();
  },
  methods: {
    getUser() {
      UserService.getUserById(this.$route.params.id)
        .then((response) => {
          this.user = response.data.result[0];
          this.created = this.user.created.toLocaleString();
          this.last_seen = this.user.last_seen.toLocaleString();
          this.$emit(
            "getUserEvent",
            this.user.first_name + " " + this.user.last_name
          );
          if (localStorage.getItem("userid") === this.$route.params.id) {
            this.show_password = true;
          }
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    toResetPassword() {
      this.$router.push("/manage/resetpassword");
    }
  },
    watch: {
    $route() {
      if(this.$route.fullPath.includes("/user/")){
        this.getUser();
      }
    },

  },
};
</script>


<style scoped>
.list {
  color: var(--blue1);

  font-size: 20px;
}
.component-body {
  background-color: rgba(255,255,255,0.7);
  border-radius: 1em;
  padding: 10px;
  margin-top: 10px;
}
.item {
  margin-bottom: 1vh;
  white-space: initial;
}
.item-text {
  margin-bottom: 1vh;
  white-space: initial;
  font-family: AddeleThin;
}

.button {
  font-size: 15px;
}
.full-button{
  margin-top: 43px;
  display: inline-block;
  width: initial;
  padding: 6px 12px;
}
.button-wrapper{
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.component-body .row{
  margin: 13px 0 0 0;
}
</style>