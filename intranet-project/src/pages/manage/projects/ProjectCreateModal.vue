<template>
  <div
    class="modal fade"
    id="createProjectModal"
    tabindex="-1"
    aria-labelledby="projectModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="projectModalLabel">
            Nieuw project aanmaken
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
                v-model="this.projectname"
                class="form-control"
                placeholder="Naam"
              />
              <textarea
                class="form-control"
                placeholder="Beschrijving"
                v-model="this.projectdescription"
              ></textarea>

              Leden toevoegen
              <SearchBar id="userSearchBar"></SearchBar>
              Overkoepelende projecten toevoegen
              <SearchBar id="parentProjectsSearchBar"></SearchBar>
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
</template>
<script>
import SearchBar from "@/shared_components/SearchBar.vue";
export default {
  name: "ProjectCreateModal",
  components: { SearchBar },
  data: function () {
    return {
      projectname: "",
      projectdescription: "",
    };
  },
  mounted() {
    var myModalEl = document.getElementById("createProjectModal");
    myModalEl.addEventListener("hidden.bs.modal", () => {
      this.clearForm();
    });
  },
  methods: {
    clearForm() {
      this.projectname = "";
      this.projectdescription = "";
    },
  },
};
</script>
<style scoped>
#createProjectModal {
  font-family: AddeleThin;
}
.modal-title {
  font-family: Montserrat;
}
input {
  margin-bottom: 10px;
}
textarea {
  margin-bottom: 10px;
}
#userSearchBar {
  margin-top: 5px;
  margin-bottom: 10px;
}
#parentProjectsSearchBar {
  margin-top: 5px;
  margin-bottom: 10px;
}
</style>
