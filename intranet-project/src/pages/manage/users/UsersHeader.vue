<template>
  <div id="usersHeader" class="container-fluid d-none d-lg-block">
    <div id="users-header-top" class="row">
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
    </div>
    <div class="row">
      <div class="full-button col-3" @click="this.$emit('sortEvent', 'name')">
        Gebruiker
        <span v-if="sortingMethod == 'name'">
          <i v-if="this.ascending" class="bi-caret-down-fill"></i>
          <i v-else class="bi-caret-up-fill"></i>
        </span>
      </div>
      <div class="full-button col" @click="this.$emit('sortEvent', 'created')">
        Geregistreerd
        <span v-if="sortingMethod == 'created'">
          <i v-if="this.ascending" class="bi-caret-down-fill"></i>
          <i v-else class="bi-caret-up-fill"></i>
        </span>
      </div>
      <div
        class="full-button col"
        @click="this.$emit('sortEvent', 'last_seen')"
      >
        Laatst gezien
        <span v-if="sortingMethod == 'last_seen'">
          <i v-if="this.ascending" class="bi-caret-down-fill"></i>
          <i v-else class="bi-caret-up-fill"></i>
        </span>
      </div>
      <div class="full-button col" @click="this.$emit('sortEvent', 'role')">
        Rol
        <span v-if="sortingMethod == 'role'">
          <i v-if="this.ascending" class="bi-caret-down-fill"></i>
          <i v-else class="bi-caret-up-fill"></i>
        </span>
      </div>
      <div
        class="full-button col"
        @click="this.$emit('sortEvent', 'amountprojects')"
      >
        Projecten
        <span v-if="sortingMethod == 'amountprojects'">
          <i v-if="this.ascending" class="bi-caret-down-fill"></i>
          <i v-else class="bi-caret-up-fill"></i>
        </span>
      </div>
      <div class="full-button col" @click="this.$emit('sortEvent', 'access')">
        Toegang
        <span v-if="sortingMethod == 'access'">
          <i v-if="this.ascending" class="bi-caret-down-fill"></i>
          <i v-else class="bi-caret-up-fill"></i>
        </span>
      </div>
      <div class="col-md-auto last-column">
        <SearchBar
          @searchBarChanged="
            (searchTerm) => $emit('searchBarChanged', searchTerm)
          "
          placeholder="Filter op naam..."
          v-bind:searchTerm="this.searchTerm"
        ></SearchBar>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from "@/shared_components/SearchBar.vue";
import PermissionService from "@/services/PermissionService.js";
export default {
  components: { SearchBar },
  name: "UsersHeader",
  props: ["searchTerm", "sortingMethod", "ascending"],
  data: function () {
    return {};
  },
  methods: {
    canCreateUser() {
      return PermissionService.userHasPermission("may_create_users");
    },
  },
};
</script>

<style scoped>
#usersHeader {
  width: 100%;
  box-sizing: border-box;
  min-height: 5vh;
  background-color: var(--blue1);
  color: white;
  font-size: 1.6vh;
}
.bi-caret-down-fill {
  margin-left: 5px;
}
.bi-caret-up-fill {
  margin-left: 5px;
}
.col {
  font-family: AddeleSemiBold;
}
#search-input {
  font-family: AddeleSemiBold;
}
#actionButton {
  width: fit-content;
  display: inline-block;
  left: 0px;
}
.last-column {
  width: 16em;
}
</style>