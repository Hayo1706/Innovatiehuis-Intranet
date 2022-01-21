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
              <div id="errorMessage">{{ errorMessage }}</div>
              <input
                v-model="this.first_name"
                class="form-control"
                id="message-text"
                placeholder="Voornaam"
                required
              />
              <input
                v-model="this.last_name"
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
              <input
                v-model="this.phone_number"
                class="form-control"
                id="message-text"
                placeholder="Telefoonnummer (optioneel)"
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
              Toegang: &nbsp;
              <select v-model="selectedScreeningState">
                <option
                  v-for="screeningstate in Object.keys(this.screeningstates)"
                  v-bind:key="screeningstate"
                >
                  {{ screeningstate }}
                </option>
              </select>
              <br />
              (De gebruiker heeft pas rechten die bij zijn rol horen, als hij
              toegang heeft gekregen.)
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="addNewUser()">
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
import { Modal } from "bootstrap";
import AlertService from "@/services/AlertService.js";
export default {
  name: "UserCreateModal",
  data: function () {
    return {
      errorMessage: "",
      modal: null,
      roles: {},
      screeningstates: {
        Geblokkeerd: 0,
        Toegestaan: 1,
      },
      selectedRole: "student",
      selectedScreeningState: "Toegestaan",

      first_name: "",
      last_name: "",
      email: "",
      phone_number: "",
      selectedRoleId: 2,
      selectedScreeningStateId: 1,
    };
  },

  mounted() {
    var myModalEl = document.getElementById("createUserModal");
    myModalEl.addEventListener("hidden.bs.modal", () => {
      this.clearForm();
    });
    this.modal = new Modal(myModalEl);
  },
  created() {
    UserService.getRoles()
      .then((response) => {
        for (const role of response) {
          this.roles[role.role_name] = role.roleid;
        }
      })
      .catch((err) => {
        AlertService.handleError(err);
      });
  },

  watch: {
    selectedRole: function (val) {
      this.selectedRoleId = this.roles[val];
    },
    selectedScreeningState: function (val) {
      this.selectedScreeningStateId = this.screeningstates[val];
    },
  },
  methods: {
    addNewUser() {
      if (!this.validateForm()) {
        return;
      }

      UserService.addUser({
        first_name: this.first_name,
        last_name: this.last_name,
        email: this.email,
        phone_number: this.phone_number,
        roleid: this.selectedRoleId,
        screening_status: this.selectedScreeningStateId,
      })
        .then((response) => {
          this.$emit("reloadUsers");
          this.closeModal();
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    setFieldEmptyErrorMessage(name) {
      this.errorMessage = 'Het veld "' + name + '" mag niet leeg zijn.';
    },
    fieldEmpty(field) {
      return field.trim() == "";
    },
    validateForm() {
      let firstNameEmpty = this.fieldEmpty(this.first_name);
      if (firstNameEmpty) {
        this.setFieldEmptyErrorMessage("Voornaam");
        return false;
      }
      let lastNameEmpty = this.fieldEmpty(this.last_name);
      if (lastNameEmpty) {
        this.setFieldEmptyErrorMessage("Achternaam");
        return false;
      }
      let emailEmpty = this.fieldEmpty(this.email);
      if (emailEmpty) {
        this.setFieldEmptyErrorMessage("Email");
        return false;
      }
      if (!this.validateEmail()) {
        this.errorMessage = "Het formaat van het emailadress is niet correct.";
        return false;
      }
      return true;
    },
    clearForm() {
      this.first_name = "";
      this.last_name = "";
      this.email = "";
      this.selectedRole = "student";
      this.selectedRoleId = 2;
      this.selectedScreeningState = "Toegestaan";
      this.selectedScreeningStateId = 0;
      this.errorMessage = "";
    },
    closeModal() {
      this.modal.hide();
    },
    validateEmail() {
      //Per the W3C HTML5 spec: https://html.spec.whatwg.org/multipage/input.html#valid-e-mail-address
      return this.email.match(
        "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
      );
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
#errorMessage {
  margin-bottom: 10px;
  color: red;
}
</style>

