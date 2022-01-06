<template>
  <div>
    
    <div id="projectFolderHeader">
      <div class="row">
        <div class="col-sm-9"><slot></slot></div>
        <div class="col-sm-2">
          <SearchBar
            @searchBarChanged="
              (searchTerm) => $emit('searchBarChanged', searchTerm)
            "
            v-bind:searchTerm="this.searchTerm"
          ></SearchBar>
        </div>
        <div class="col-sm-1">
          <button
            class="iconButton"
            data-bs-toggle="modal"
            data-bs-target="#folderModal"
          >
            <img class="iconImage" src=".\..\..\assets\images\add_icon.png" />
          </button>
        </div>
      </div>
    </div>

    <div
      class="modal fade"
      id="folderModal"
      tabindex="-1"
      aria-labelledby="folderModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="folderModalLabel">
              Nieuwe map aanmaken
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
                <input
                  v-model="this.newFolderName"
                  class="form-control"
                  id="message-text"
                  placeholder="Nieuwe_Map"
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
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import SearchBar from "@/shared_components/SearchBar.vue";
export default {
  name: "ProjectFolderHeader",
  components: {
    SearchBar,
  },
  props: ["path"],
  data: function () {
    return {
      newFolderName: null,
    };
  },
  methods: {
    addNewFolder() {
      if (this.newFolderName == null) {
        this.newFolderName = "Nieuwe_Map";
      }
      FilestorageService.createFolder(
        this.$route.params.id,
        this.path,
        this.newFolderName
      )
        .then(() => {
          this.$emit("newFolderAdded");
          this.newFolderName = null;
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    reload() {
      console.log("updating key");
      this.$emit("reload");
    },
  },
};
</script>

<style scoped>
#projectFolderHeader {
  color: white;
  font-size: calc(1vw + 1vh);
  font-family: AddeleSemiBold;
  margin: calc(1vw + 1vh);
  text-align: left;
  background-color: var(--blue1);
}
.iconButton {
  border: 0;
  background-color: transparent;
}
.iconImage {
  height: calc(1vw + 1vh);
  margin: 0 auto;
  display: block;
}
.input-group {
  margin: 0.5vh auto;
  height: 80%;
}
</style>