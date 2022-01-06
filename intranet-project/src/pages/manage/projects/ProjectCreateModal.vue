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
              <div id="errorMessage">{{ errorMessage }}</div>
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
              <br />
              <span
                id="selectedUserList"
                v-for="user in selectedUsers"
                v-bind:key="user.userid"
                >{{ user.first_name }} {{ user.last_name }},&nbsp;</span
              >
              <SearchBar
                id="userSearchBar"
                v-bind:searchTerm="this.userSearchTerm"
                @searchBarChanged="
                  (searchTerm) => {
                    handleSearchUser(searchTerm);
                  }
                "
              ></SearchBar>

              <div class="dropdown-menu" id="userDropdown">
                <div
                  class="dropdown-item"
                  v-for="user in filteredUsers"
                  v-bind:key="user.userid"
                  @click="selectUser(user)"
                >
                  {{ user.first_name }} {{ user.last_name }}
                </div>
              </div>
              Overkoepelende projecten toevoegen
              <SearchBar
                id="parentProjectsSearchBar"
                v-bind:searchTerm="this.parentSearchTerm"
                @searchBarChanged="
                  (searchTerm) => {
                    this.parentSearchTerm = searchTerm;
                    handleSearchParent(searchTerm);
                  }
                "
              ></SearchBar>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-primary"
            @click="addNewProject()"
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
import UserService from "@/services/UserService.js";
import { Modal } from "bootstrap";
export default {
  name: "ProjectCreateModal",
  components: { SearchBar },
  data: function () {
    return {
      modal: null,
      projectname: "",
      projectdescription: "",
      userSearchTerm: "",
      parentSearchTerm: "",
      errorMessage: "",

      users: [],
      filteredUsers: [],
      selectedUsers: [],
    };
  },
  mounted() {
    var myModalEl = document.getElementById("createProjectModal");
    myModalEl.addEventListener("hidden.bs.modal", () => {
      this.clearForm();
    });
    myModalEl.addEventListener("show.bs.modal", () => {
      UserService.getUsers()
        .then((response) => {
          this.users = response;
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    });
    this.modal = new Modal(myModalEl);
  },
  methods: {
    closeModal() {
      this.modal.hide();
    },
    fieldEmpty(field) {
      return field.trim() == "";
    },
    addNewProject() {
      if (!this.validateForm()) {
        return;
      }
      this.closeModal();
    },
    validateForm() {
      let projectNameEmpty = this.fieldEmpty(this.projectname);
      if (projectNameEmpty) {
        this.setFieldEmptyErrorMessage("Naam");
        return false;
      }
      let description = this.fieldEmpty(this.projectdescription);
      if (description) {
        this.setFieldEmptyErrorMessage("Beschrijving");
        return false;
      }
      return true;
    },

    handleSearchUser(name) {
      if (name) {
        this.userSearchTerm = name;
        this.filteredUsers = this.getFilteredUsers();
      } else {
        this.filteredUsers = [];
      }
    },
    selectUser(user) {
      this.userSearchTerm = "";
      this.filteredUsers = [];
      this.selectedUsers.push(user);
      console.log(this.selectedUsers);
    },
    getFilteredUsers() {
      return this.users.filter((item) => {
        return (
          (item.first_name + " " + item.last_name)
            .toLowerCase()
            .includes(this.userSearchTerm.toLowerCase()) &&
          !this.selectedUsersContainsUser(item.userid)
        );
      });
    },
    selectedUsersContainsUser(userid) {
      for (const user of this.selectedUsers) {
        if (user.userid == userid) {
          return true;
        }
      }
      return false;
    },
    handleSearchParent(name) {
      if (name) {
        console.log(name);
      }
    },
    setFieldEmptyErrorMessage(name) {
      this.errorMessage = 'Het veld "' + name + '" mag niet leeg zijn.';
    },
    clearForm() {
      this.projectname = "";
      this.projectdescription = "";
      this.userSearchTerm = "";
      this.parentSearchTerm = "";

      this.selectedUsers = [];
      this.errorMessage = "";
    },
  },
  watch: {
    filteredUsers: function () {
      if (this.filteredUsers.length == 0) {
        document.getElementById("userDropdown").classList.remove("show");
      } else {
        document.getElementById("userDropdown").classList.add("show");
      }
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
  height: 20vh;
}
#userSearchBar {
  margin-top: 5px;
  margin-bottom: 10px;
}
#parentProjectsSearchBar {
  margin-top: 5px;
  margin-bottom: 10px;
}
#selectedUserList {
  font-family: AddeleThin;
}
#errorMessage {
  margin-bottom: 10px;
  color: red;
}
</style>
