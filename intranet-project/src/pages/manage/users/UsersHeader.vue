<template>
  <div id="usersHeader" class="container-fluid d-none d-lg-block">
    <div class="row">
      <div class="col">Gebruiker</div>
      <div class="col">Geregistreerd</div>
      <div class="col">Laatst gezien</div>
      <div class="col">Rol</div>
      <div class="col">Projecten</div>
      <div class="col">Screening</div>
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
  props: ["searchTerm"],
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
  min-height: 10vh;
  background-color: var(--blue1);
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
  font-family: Monserrat;
}
.input-group {
  width: 90%;
}
#search-input {
  margin-right: 4px;
}
img {
  width: calc(2vw + 3vh);
  padding-bottom: 10px;
  padding-left: 10px;
  cursor: pointer;
}
</style>