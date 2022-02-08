<template>
  <div id="usersHeader" class="container-fluid d-none d-lg-block">
    <div id="users-header-top" class="row">
      <button
        id="addUser"
        class="full btn pmd-btn-fab pmd-ripple-effect btn-primary"
        data-bs-toggle="modal"
        data-bs-target="#createUserModal"
        type="button"
        v-show="canCreateUser()"
      >
        <img src="@/assets/images/plus2.png">
        <i class="material-icons pmd-sm">Gebruiker toevoegen</i>
      </button>
    </div>
    <div class="row">
      <div class="column-title col-3" @click="this.$emit('sortEvent', 'name')">
        Gebruiker
        <span v-if="sortingMethod == 'name'">
          <i v-if="this.ascending" class="bi-caret-down-fill"></i>
          <i v-else class="bi-caret-up-fill"></i>
        </span>
      </div>
      <div class="column-title col" @click="this.$emit('sortEvent', 'created')">
        Geregistreerd
        <span v-if="sortingMethod == 'created'">
          <i v-if="this.ascending" class="bi-caret-down-fill"></i>
          <i v-else class="bi-caret-up-fill"></i>
        </span>
      </div>
      <div
        class="column-title col"
        @click="this.$emit('sortEvent', 'last_seen')"
      >
        Laatst gezien
        <span v-if="sortingMethod == 'last_seen'">
          <i v-if="this.ascending" class="bi-caret-down-fill"></i>
          <i v-else class="bi-caret-up-fill"></i>
        </span>
      </div>
      <div class="column-title col" @click="this.$emit('sortEvent', 'role')">
        Rol
        <span v-if="sortingMethod == 'role'">
          <i v-if="this.ascending" class="bi-caret-down-fill"></i>
          <i v-else class="bi-caret-up-fill"></i>
        </span>
      </div>
      <div
        class="column-title col"
        @click="this.$emit('sortEvent', 'amountprojects')"
      >
        Projecten
        <span v-if="sortingMethod == 'amountprojects'">
          <i v-if="this.ascending" class="bi-caret-down-fill"></i>
          <i v-else class="bi-caret-up-fill"></i>
        </span>
      </div>
      <div class="column-title col" @click="this.$emit('sortEvent', 'access')">
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
  background: hsl(0deg 0% 98% / 90%);
  color: white;
  font-size: 1.6vh;
  padding: 11px 0 0 0;
  border-bottom: 2px solid hsl(225deg 7% 89%);
}
#search-input {
  font-family: AddeleThin;
  border-style: solid;
}
.column-title {
  font-size: 16pt;
  text-align: center;
  background: rgb(224 224 224);
  border: 1px solid #d4d4d4;
  border-bottom: 0px;
}
.column-title:hover {
  cursor: pointer;
  background: rgb(216, 216, 216);
}
img {
  filter: invert(1);
  width: 3vh;
  margin: 0 8px 4px 0;
  cursor: pointer;
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
#usersHeader .full-button {
  margin: 0;
}
#addUser {
  background-color: var(--blue2);
  width: fit-content;
  display: inline-block;
  left: 0px;
  margin-left: 13px;
  padding-bottom: 3px;
}
#addUser div{
  color: white;
}
#users-header-top{
  padding-bottom: 11px;
  margin: 0;
}
.form-switch{
  margin-left: auto;
  display: flex;
  align-items: flex-end;
}
.input-group{
  margin: 0 !important;
}
</style>