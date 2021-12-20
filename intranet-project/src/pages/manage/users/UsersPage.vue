<template>
  <div>
    <button
      id="actionButton"
      class="btn pmd-btn-fab pmd-ripple-effect btn-primary"
      type="button"
    >
      <i class="material-icons pmd-sm">Gebruiker toevoegen</i>
    </button>
    <UsersHeader
      @searchBarChanged="setSearchTerm"
      v-bind:searchTerm="this.searchTerm"
    ></UsersHeader>
    <div class="container-fluid d-sm-block d-lg-none">
      <div class="row">
        <SearchBar
          class="col"
          id="searchBarMobile"
          @searchBarChanged="setSearchTerm"
          v-bind:searchTerm="this.searchTerm"
        ></SearchBar>
        <hr />
      </div>
    </div>
    <div class="container-fluid">
      <div v-for="user of filteredUsers" :key="user.firstname">
        <UserListing v-bind:user="user"></UserListing>
      </div>
      <div id="noresults" v-if="filteredUsers.length == 0">
        Geen resultaten.
      </div>
    </div>
    <div id="littleSpace"></div>
  </div>
</template>

<script>
import UserService from "@/services/UserService.js";
import UsersHeader from "./UsersHeader.vue";
import SearchBar from "@/shared_components/SearchBar.vue";
import UserListing from "./UserListing.vue";
export default {
  components: {
    UsersHeader,
    SearchBar,
    UserListing,
  },
  name: "ProjectsPage",
  data: function () {
    return {
      users: [],
      searchTerm: null,
    };
  },
  methods: {
    setSearchTerm(value) {
      this.searchTerm = value;
    },
    shouldShow(item) {
      let shouldShow = false;
      shouldShow = this.matchesSearchTermWhenShould(item);
      return shouldShow;
    },
    matchesSearchTermWhenShould(item) {
      if (this.searchTerm == null) {
        return true;
      } else {
        return (item.firstname +" "+ item.lastname)
          .toLowerCase()
          .includes(this.searchTerm.toLowerCase());
      }
    },
  },

  computed: {
    filteredUsers() {
      return this.users.filter((item) => {
        return this.shouldShow(item);
      });
    },
  },
  async created() {
    this.$emit("newHeaderTitle", "Gebruikers - Overzicht");
    UserService.getUsers()
      .then((response) => {
        this.users = response;
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });
  },
};
</script>

<style scoped>
#searchBarMobile {
  padding-top: 5px;
  margin-top: 5px;
  margin-bottom: 5px;
  width: 100%;
}
#noresults {
  margin-top: 10px;
}
#actionButton {
  position: fixed;
  bottom: 0;
  left: 0;
  margin: 20px;
  background-color: var(--gold1);
  border-color: var(--blue1);
}
#littleSpace {
  height: 60px;
  width: 100%;
}
</style>