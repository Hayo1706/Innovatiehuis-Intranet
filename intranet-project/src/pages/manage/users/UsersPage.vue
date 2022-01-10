<template>
  <div class="container-fluid">
    <button
      id="actionButton"
      class="full btn pmd-btn-fab pmd-ripple-effect btn-primary"
      data-bs-toggle="modal"
      data-bs-target="#createUserModal"
      type="button"
      v-show="canCreateUser()"
    >
      <i class="material-icons pmd-sm">Gebruiker toevoegen</i>
    </button>

    <UsersHeader
      class="component-header"
      @searchBarChanged="setSearchTerm"
      v-bind:searchTerm="this.searchTerm"
    ></UsersHeader>
    <UserCreateModal></UserCreateModal>
    <div class="container-fluid d-sm-block d-lg-none">
      <div class="row">
        <SearchBar
          class="col"
          id="searchBarMobile"
          @searchBarChanged="setSearchTerm"
          v-bind:searchTerm="this.searchTerm"
        ></SearchBar>
      </div>
    </div>
    <div class="container-fluid">
      <div v-for="user of filteredUsers" :key="user.first_name">
        <UserListing
          v-bind:user="user"
          @removeUser="this.removeUser"
        ></UserListing>
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
import UserCreateModal from "./UserCreateModal.vue";
import PermissionService from "@/services/PermissionService.js";
export default {
  components: {
    UsersHeader,
    SearchBar,
    UserListing,
    UserCreateModal,
  },
  name: "ProjectsPage",
  data: function () {
    return {
      users: [],
      searchTerm: null,
    };
  },
  methods: {
    canCreateUser() {
      return PermissionService.userHasPermission("may_create_users");
    },
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
        return (item.first_name + " " + item.last_name)
          .toLowerCase()
          .includes(this.searchTerm.toLowerCase());
      }
    },
    removeUser(userid) {
      this.users = this.users.filter(function (item) {
        return item.userid !== userid;
      });
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
  color: white;
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