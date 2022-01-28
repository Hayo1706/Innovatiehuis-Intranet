<template>
  <div class="container-fluid">
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css"
    />
    <button
      id="actionButton"
      class="full btn pmd-btn-fab pmd-ripple-effect btn-primary d-lg-none"
      data-bs-toggle="modal"
      data-bs-target="#createUserModal"
      type="button"
      v-show="canCreateUser()"
    >
      <i class="material-icons pmd-sm">Gebruiker toevoegen</i>
    </button>

    <UsersHeader
      v-bind:sortingMethod="this.sortingMethod"
      v-bind:ascending="this.ascending"
      @sortEvent="
        (sortingTerm) => {
          sort(sortingTerm);
        }
      "
      class="component-header"
      @searchBarChanged="setSearchTerm"
      v-bind:searchTerm="this.searchTerm"
    ></UsersHeader>

    <div class="container-fluid d-sm-block d-lg-none" id="sorting_space">
      <p>Sorteren op:</p>
      <div class="row">
        <button class="full-button col-3" @click="sort('name')">
          Naam
          <span v-if="sortingMethod == 'name'"
            ><i v-if="this.ascending" class="bi-caret-down-fill"></i
            ><i v-else class="bi-caret-up-fill"></i
          ></span>
        </button>
        <button class="full-button col-3" @click="sort('email')">
          Email
          <span v-if="sortingMethod == 'email'"
            ><i v-if="this.ascending" class="bi-caret-down-fill"></i
            ><i v-else class="bi-caret-up-fill"></i
          ></span>
        </button>
        <button class="full-button col-3" @click="sort('phone')">
          Telefoonnummer
          <span v-if="sortingMethod == 'phone'"
            ><i v-if="this.ascending" class="bi-caret-down-fill"></i
            ><i v-else class="bi-caret-up-fill"></i
          ></span>
        </button>

        <button class="full-button col-3" @click="sort('created')">
          Registreerdatum
          <span v-if="sortingMethod == 'created'"
            ><i v-if="this.ascending" class="bi-caret-down-fill"></i
            ><i v-else class="bi-caret-up-fill"></i
          ></span>
        </button>
        <button class="full-button col-3" @click="sort('last_seen')">
          Laatst gezien
          <span v-if="sortingMethod == 'last_seen'"
            ><i v-if="this.ascending" class="bi-caret-down-fill"></i
            ><i v-else class="bi-caret-up-fill"></i
          ></span>
        </button>
        <button class="full-button col-3" @click="sort('role')">
          Rol
          <span v-if="sortingMethod == 'role'"
            ><i v-if="this.ascending" class="bi-caret-down-fill"></i
            ><i v-else class="bi-caret-up-fill"></i
          ></span>
        </button>
        <button class="full-button col-3" @click="sort('amountprojects')">
          Aantal projecten
          <span v-if="sortingMethod == 'amountprojects'"
            ><i v-if="this.ascending" class="bi-caret-down-fill"></i
            ><i v-else class="bi-caret-up-fill"></i
          ></span>
        </button>
        <button class="full-button col-3" @click="sort('access')">
          Toegang
          <span v-if="sortingMethod == 'access'"
            ><i v-if="this.ascending" class="bi-caret-down-fill"></i
            ><i v-else class="bi-caret-up-fill"></i
          ></span>
        </button>
      </div>
    </div>
    <UserCreateModal @reloadUsers="loadUsers()"></UserCreateModal>
    <div class="container-fluid d-sm-block d-lg-none">
      <div class="row">
        <SearchBar
          class="col"
          id="searchBarMobile"
          @searchBarChanged="setSearchTerm"
          placeholder="Zoek gebruikers..."
          v-bind:searchTerm="this.searchTerm"
        ></SearchBar>
      </div>
    </div>
    <div class="listing-container container-fluid">
      <div v-for="user of filteredUsers" :key="user.userid">
        <UserListing
          v-bind:user="user"
          v-bind:all_roles="roles"
          @removeUser="this.removeUser"
          @accessChanged="setUserAccess"
          @roleChanged="setUserRole"
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
import AlertService from "@/services/AlertService.js";
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
      sortingMethod: "name",
      ascending: true,
      roles: [],
    };
  },
  methods: {
    setUserAccess(id, new_access_id) {
      this.users.find((user) => user.userid == id).screening_status =
        new_access_id;
    },
    setUserRole(id, new_role_id) {
      this.users.find((user) => user.userid == id).roleid = new_role_id;
    },
    sort(method) {
      if (this.sortingMethod != method) {
        this.sortingMethod = method;
        this.ascending = true;
      } else {
        this.ascending = !this.ascending;
      }
    },
    canCreateUser() {
      return PermissionService.userHasPermission("may_create_users");
    },
    setSearchTerm(value) {
      this.searchTerm = value;
    },
    shouldShow(item) {
      return this.matchesSearchTermWhenShould(item);
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
    loadUsers() {
      UserService.getUsers()
        .then((response) => {
          this.users = response.data.result;
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    removeUser(userid) {
      this.users = this.users.filter(function (item) {
        return item.userid !== userid;
      });
    },
    sortingFunction(a, b) {
      if (this.ascending) {
        if (a < b) {
          return -1;
        }
        if (a > b) {
          return 1;
        }
      } else {
        if (a > b) {
          return -1;
        }
        if (a < b) {
          return 1;
        }
      }
      return 0;
    },
  },

  computed: {
    filteredUsers() {
      let filteredUsers = this.users.filter((item) => {
        return this.shouldShow(item);
      });
      if (this.sortingMethod == "name") {
        filteredUsers = filteredUsers.sort((a, b) => {
          let fa = a.first_name.toLowerCase() + " " + a.last_name.toLowerCase(),
            fb = b.first_name.toLowerCase() + " " + b.last_name.toLowerCase();
          return this.sortingFunction(fa, fb);
        });
      } else if (this.sortingMethod == "created") {
        filteredUsers = filteredUsers.sort((a, b) => {
          let fa = a.created,
            fb = b.created;
          return this.sortingFunction(fa, fb);
        });
      } else if (this.sortingMethod == "email") {
        filteredUsers = filteredUsers.sort((a, b) => {
          let fa = a.email,
            fb = b.email;
          return this.sortingFunction(fa, fb);
        });
      } else if (this.sortingMethod == "phone") {
        filteredUsers = filteredUsers.sort((a, b) => {
          let fa = a.phone_number,
            fb = b.phone_number;
          return this.sortingFunction(fa, fb);
        });
      } else if (this.sortingMethod == "last_seen") {
        filteredUsers = filteredUsers.sort((a, b) => {
          let fa = a.last_seen,
            fb = b.last_seen;
          return this.sortingFunction(fa, fb);
        });
      } else if (this.sortingMethod == "role") {
        filteredUsers = filteredUsers.sort((a, b) => {
          let fa = a.roleid,
            fb = b.roleid;
          return this.sortingFunction(fa, fb);
        });
      } else if (this.sortingMethod == "amountprojects") {
        filteredUsers = filteredUsers.sort((a, b) => {
          let fa = a.amountprojects,
            fb = b.amountprojects;
          return this.sortingFunction(fa, fb);
        });
      } else if (this.sortingMethod == "access") {
        filteredUsers = filteredUsers.sort((a, b) => {
          let fa = a.screening_status,
            fb = b.screening_status;
          return this.sortingFunction(fa, fb);
        });
      }
      return filteredUsers;
    },
  },
  created() {
    UserService.getRoles()
      .then((response) => {
        this.roles = response.data.result;
        AlertService.handleSuccess(response);
      })
      .catch((err) => {
        AlertService.handleError(err);
      });
    this.$emit("newHeaderTitle", "Gebruikers - Overzicht");
    this.loadUsers();
  },
};
</script>

<style scoped>
#sorting_space {
  padding: 20px;
  box-sizing: border-box;
  color: var(--blue1);
  overflow: visible;
  background: linear-gradient(
    to right top,
    rgba(230, 230, 230, 0.7),
    rgba(230, 230, 230, 0.9)
  );
  border-radius: 1rem;
  margin-bottom: 1vh;
  font-size: 1.7vh;
  border: solid var(--gold1) 2px;
}
#searchBarMobile {
  padding-top: 5px;
  margin-top: 5px;
  margin-bottom: 5px;
  width: 100%;
}
.listing-container {
  padding: 0;
  border-radius: 0px 0px 10px 10px;
  background-color: rgba(255, 255, 255, 0.3);
}
#noresults {
  margin: 10px;
  color: white;
}
#actionButton {
  position: fixed;
  bottom: 0;
  right: 0;
  margin: 20px;
  background-color: var(--gold1);
  border-color: var(--blue1);
}
#littleSpace {
  height: 60px;
  width: 100%;
}
.full-button {
  display: inline;
  width: fit-content;
}
p {
  font-family: AddeleSemiBold;
  font-size: 20px;
}
.bi-caret-down-fill {
  margin-left: 5px;
}
.bi-caret-up-fill {
  margin-left: 5px;
}
</style>