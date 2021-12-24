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
              <!-- TODO add input here-->
              <input
                v-model="this.projectname"
                class="form-control"
                id="message-text"
                placeholder="Naam van project"
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
</template>
<script>
export default {
  name: "ProjectCreateModal",
  data: function () {
    return {
      projectname: "",
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
    },
  },
};
</script>

