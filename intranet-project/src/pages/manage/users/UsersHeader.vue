<template>
  <div id="usersHeader" class="container-fluid d-none d-lg-block">
    <div class="row">
      <div class="full-button col" @click="this.$emit('sortEvent', 'name')">
        Gebruiker
        <span v-if="sortingMethod == 'name'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>

      <div class="full-button col" @click="this.$emit('sortEvent', 'created')">
        Geregistreerd
        <span v-if="sortingMethod == 'created'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>
      <div
        class="full-button col"
        @click="this.$emit('sortEvent', 'last_seen')"
      >
        Laatst gezien
        <span v-if="sortingMethod == 'last_seen'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>
      <div class="full-button col" @click="this.$emit('sortEvent', 'role')">
        Rol
        <span v-if="sortingMethod == 'role'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>
      <div
        class="full-button col"
        @click="this.$emit('sortEvent', 'amountprojects')"
      >
        Projecten
        <span v-if="sortingMethod == 'amountprojects'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>
      <div
        class="full-button col"
        @click="this.$emit('sortEvent', 'screening')"
      >
        Screening
        <span v-if="sortingMethod == 'screening'"
          ><i v-if="this.ascending" class="bi-caret-down-fill"></i
          ><i v-else class="bi-caret-up-fill"></i
        ></span>
      </div>
      <div class="col">
        <SearchBar
          @searchBarChanged="
            (searchTerm) => $emit('searchBarChanged', searchTerm)
          "
          v-bind:searchTerm="this.searchTerm"
        ></SearchBar>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from "@/shared_components/SearchBar.vue";
export default {
  components: { SearchBar },
  name: "UsersHeader",
  props: ["searchTerm", "sortingMethod", "ascending"],
  data: function () {
    return {};
  },
  methods: {},
};
</script>

<style scoped>
#usersHeader {
  width: 100%;
  box-sizing: border-box;
  min-height: 13vh;
  background-color: var(--blue1);
  border: white 5px solid;
  margin-top: 1vh;
  color: white;
  font-size: 1.6vh;

  padding: 20px;

  margin-bottom: 1vh;
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
</style>