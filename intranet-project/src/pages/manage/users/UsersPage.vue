<template>
  <div>
    <div id="descriptionbar" class="d-none d-lg-flex">
      <span>Gebruiker</span>
      <span>Geregistreerd</span>
      <span>Laatst gezien</span>
      <span>Rol</span>
      <span>Projecten</span>
      <span>Screening</span>
    </div>
    <div id="userlist" v-for="user of users" :key="user.name">
      <UserListing
        v-bind:id="user.userid"
        v-bind:name="user.name"
        v-bind:created="user.registrationdate"
        v-bind:lastModified="user.lastseen"
        v-bind:role="user.role"
        v-bind:projects="user.projects"
        v-bind:screening="user.screening"
        v-on:reload="reload()"
      />
      <br />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import UserListing from './UserListing.vue';

export default {
  components: { UserListing },
  name: "UsersPage",
  data: function () {
    return { users: [] };
  },
  methods: {
    reload() {
      axios
        .get("http://94.212.125.203:5000/api/users")
        .then((response) => {
          this.users = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  created() {
    this.reload();
    this.$emit("loaded", "Gebruikers - Overzicht");
  },
};
</script>

<style>
#descriptionbar {
  width: 100%;
  box-sizing: border-box;
  min-height: 10vh;
  background-color: #28418a;
  border: white 5px solid;
  margin-top: 1vh;
  color: white;
  font-size: calc(1vw + 1vh);
  padding: 20px;

  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-basis: 100%;
  gap: 60px;
  font-family: AddeleSemiBold;
}

#userlist {
  width: 100%;
  box-sizing: border-box;
  border-left: white 5px solid;
  border-right: white 5px solid;
  color: white;
  font-size: calc(1vw + 1vh);
  padding: 1vw;
  font-family: AddeleThin;
}

span {
  flex: 1 1 0;
  width: 0;
  overflow-wrap: anywhere;
}
</style>