<template>
  <div>
    <button
      id="actionButton"
      class="btn pmd-btn-fab pmd-ripple-effect btn-primary"
      data-bs-toggle="modal"
      data-bs-target="#createUserModal"
      type="button"
    >
      <i class="material-icons pmd-sm">Gebruiker toevoegen</i>
    </button>
    <UsersHeader
      @searchBarChanged="setSearchTerm"
      v-bind:searchTerm="this.searchTerm"
    ></UsersHeader>
    <div
      class="modal fade"
      id="createUserModal"
      tabindex="-1"
      aria-labelledby="userModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="userModalLabel">
              Nieuwe gebruiker toevoegen
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-9">
                <!-- TODO add input here-->
                <input
                  v-model="this.newFolderName"
                  class="form-control"
                  id="message-text"
                  placeholder="Nieuwe Map"
                />
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-primary"
              data-bs-dismiss="modal"
              @click="addNewFolder()"
            >
              Toevoegen
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Annuleren
            </button>
          </div>
        </div>
      </div>
    </div>

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
        return (item.firstname + " " + item.lastname)
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