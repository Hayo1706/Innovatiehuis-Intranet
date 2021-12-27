<template>
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
                v-model="this.firstname"
                class="form-control"
                id="message-text"
                placeholder="Voornaam"
              />
              <input
                v-model="this.lastname"
                class="form-control"
                id="message-text"
                placeholder="Achternaam"
              />
              <input
                v-model="this.email"
                class="form-control"
                id="message-text"
                placeholder="Email"
              />
              Rol: &nbsp;
              <select v-model="selectedRole">
                <option
                  v-for="role in Object.keys(this.roles)"
                  v-bind:key="role"
                >
                  {{ role }}
                </option>
              </select>
              <br />
              Screeningstatus: &nbsp;
              <select v-model="selectedScreeingstate">
                <option
                  v-for="screeningstate in Object.keys(this.screeningstates)"
                  v-bind:key="screeningstate"
                >
                  {{ screeningstate }}
                </option>
              </select>
              <br />
              (De gebruiker heeft pas rechten die bij zijn rol horen, als de
              screening voltooid is.)
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-primary"
            data-bs-dismiss="modal"
            @click="addNewUser()"
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
import UserService from "@/services/UserService.js";
export default {
  name: "UserCreateModal",
  data: function () {
    return {
      roles: { observer: 1, student: 2, moderator: 3, admin: 4 },
      screeningstates: {
        "nog niet in behandeling": 0,
        "in behandeling": 1,
        voltooid: 2,
      },
      selectedRole: "student",
      selectedScreeingstate: "nog niet in behandeling",

      firstname: "",
      lastname: "",
      email: "",
      selectedRoleId: 2,
      selectedScreeingstateId: 0,
    };
  },

  mounted() {
    var myModalEl = document.getElementById("createUserModal");
    myModalEl.addEventListener("hidden.bs.modal", () => {
      this.clearForm();
    });
  },

  watch: {
    selectedRole: function (val) {
      this.selectedRoleId = this.roles[val];
    },
    selectedScreeingstate: function (val) {
      this.selectedScreeingstateId = this.screeningstates[val];
    },
  },
  methods: {
    addNewUser() {
      UserService.addUser(this.user)
        .then(() => {})
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    clearForm() {
      this.firstname = "";
      this.lastname = "";
      this.email = "";
      this.selectedRole = "student";
      this.selectedRoleId = 2;
      this.selectedScreeingstate = "nog niet in behandeling";
      this.selectedScreeingstateId = 0;
    },
  },
};
</script>
<style  scoped>
input {
  margin-bottom: 10px;
}
select {
  margin-bottom: 10px;
  border-radius: 0.25rem;
}
#createUserModal {
  font-family: AddeleThin;
}
.modal-title {
  font-family: Montserrat;
}
</style>

