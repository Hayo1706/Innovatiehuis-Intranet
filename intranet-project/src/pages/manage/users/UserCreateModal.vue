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
              <select v-model="selected_access_state">
                <option
                  v-for="access in Object.keys(this.access_states)"
                  v-bind:key="access"
                >
                  {{ access }}
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
      access_states: {
        Geblokkeerd: 0,
        Toegestaan: 1,
      },
      selectedRole: "",

      previous_access_state: "",
      selected_access_state: "Toegestaan",

      first_name: "",
      last_name: "",
      email: "",
      phone_number: "",
      selectedRoleId: 2,
      selectedAccessId: 1,
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
        console.log({ response });
        for (const role of response.data.result) {
          if (
            role.power_level <=
            localStorage.getItem("may_cud_users_with_power_level_up_to")
          ) {
            this.roles[role.role_name] = role.roleid;
          }
        }
        this.selectedRole = Object.keys(this.roles)[0];
        this.selectedRoleId = this.roles[this.selectedRole];
        AlertService.handleSuccess(response);
      })
      .catch((err) => {
        AlertService.handleError(err);
      });
  },

  watch: {
    selectedRole: function (val) {
      this.selectedRoleId = this.roles[val];
    },
    selected_access_state: function (val) {
      this.selectedAccessId = this.access_states[val];
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
        access_status: this.selectedAccessId,
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
      this.selectedRole = Object.keys(this.roles)[0];
      this.selectedRoleId = this.roles[this.selectedRole];
      this.selected_access_state = "Toegestaan";
      this.selectedAccessId = 1;
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

