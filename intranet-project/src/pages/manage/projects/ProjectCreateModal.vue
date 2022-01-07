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
          <form autocomplete="off">
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
                >{{ user.first_name }} {{ user.last_name }}&nbsp;<button
                  @click="this.unselectUser(user.userid)"
                  class="entryDeleteButton"
                >
                  x</button
                >,&nbsp;</span
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
              <br />
              <span
                id="selectedParentList"
                v-for="project in selectedParents"
                v-bind:key="project.projectid"
                >{{ project.project_name }}&nbsp;<button
                  @click="this.unselectParent(project.projectid)"
                  class="entryDeleteButton"
                >
                  x</button
                >,&nbsp;</span
              >
              <SearchBar
                id="parentProjectsSearchBar"
                v-bind:searchTerm="this.parentSearchTerm"
                @searchBarChanged="
                  (searchTerm) => {
                    handleSearchParent(searchTerm);
                  }
                "
              ></SearchBar>

              <div class="dropdown-menu" id="parentDropdown">
                <div
                  class="dropdown-item"
                  v-for="project in filteredParents"
                  v-bind:key="project.projectid"
                  @click="selectParent(project)"
                >
                  {{ project.project_name }}
                </div>

                
              </div>
                            Sub-projecten toevoegen
              <br />
              <span
                id="selectedChildList"
                v-for="project in selectedChildren"
                v-bind:key="project.projectid"
                >{{ project.project_name }}&nbsp;<button
                  @click="this.unselectChild(project.projectid)"
                  class="entryDeleteButton"
                >
                  x</button
                >,&nbsp;</span
              >
              <SearchBar
                id="childProjectsSearchBar"
                v-bind:searchTerm="this.childSearchTerm"
                @searchBarChanged="
                  (searchTerm) => {
                    handleSearchChild(searchTerm);
                  }
                "
              ></SearchBar>

              <div class="dropdown-menu" id="childDropdown">
                <div
                  class="dropdown-item"
                  v-for="project in filteredChildren"
                  v-bind:key="project.projectid"
                  @click="selectChild(project)"
                >
                  {{ project.project_name }}
                </div>

                
              </div>
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
import ProjectService from "@/services/ProjectService.js";
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
      childSearchTerm: "",
      errorMessage: "",

      users: [],
      filteredUsers: [],
      selectedUsers: [],

      parents: [],
      filteredParents: [],
      selectedParents: [],

      children: [],
      filteredChildren: [],
      selectedChildren: []
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
      ProjectService.getProjects()
        .then((response) => {
          this.parents = response;
          this.children = response;
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
            const memberIds = this.getUserIds(this.selectedUsers);
            const parentIds = this.getProjectIds(this.selectedParents);
            const childIds = this.getProjectIds(this.selectedChildren);

            console.log(memberIds);
            console.log(parentIds);
            console.log(childIds);

            const project = {"project_name": this.projectname, "description":this.projectdescription};
       ProjectService.addProject(project)
        .then(() => {
          alert("Het project \""+this.projectname+"\" is aangemaakt!");
          window.location.reload();
          
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
            this.closeModal();

          alert("Er ging iets mis bij het aanmaken van een project, probeer later weer");
        });



        
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
    },
    unselectUser(userid) {
      this.selectedUsers = this.selectedUsers.filter((item) => {
        return item.userid != userid;
      });
      if (this.userSearchTerm) {
        this.filteredUsers = this.getFilteredUsers();
      }
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
    selectedParentsContainsParent(projectid) {
      for (const project of this.selectedParents) {
        if (project.projectid == projectid) {
          return true;
        }
      }
      return false;
    },
    
    selectedChildrenContainsChild(projectid){
       for (const project of this.selectedChildren) {
        if (project.projectid == projectid) {
          return true;
        }
      }
      return false;
    },
    handleSearchParent(name) {
      if (name) {
        this.parentSearchTerm = name;
        this.filteredParents = this.getFilteredParents();
      } else {
        this.filteredParents = [];
      }
    },
    getFilteredParents() {
      return this.parents.filter((item) => {
        return (
          item.project_name
            .toLowerCase()
            .includes(this.parentSearchTerm.toLowerCase()) &&
          !this.selectedParentsContainsParent(item.projectid)
        );
      });
    },

    selectParent(project) {
      this.parentSearchTerm = "";
      this.filteredParents = [];
      this.selectedParents.push(project);
    },
    unselectParent(projectid) {
      this.selectedParents = this.selectedParents.filter((item) => {
        return item.projectid != projectid;
      });
      if (this.parentSearchTerm) {
        this.filteredParents = this.getFilteredParents();
      }
    },
    handleSearchChild(name) {
      if (name) {
        this.childSearchTerm = name;
        this.filteredChildren = this.getFilteredChildren();
      } else {
        this.filteredChildren = [];
      }
    },
    selectChild(project) {
      this.childSearchTerm = "";
      this.filteredChildren = [];
      this.selectedChildren.push(project);
    },
    unselectChild(projectid) {
      this.selectedChildren = this.selectedChildren.filter((item) => {
        return item.projectid != projectid;
      });
      if (this.childSearchTerm) {
        this.filteredChildren = this.getFilteredChildren();
      }
    },
    getFilteredChildren() {
      return this.children.filter((item) => {
        return (
          item.project_name
            .toLowerCase()
            .includes(this.childSearchTerm.toLowerCase()) &&
          !this.selectedChildrenContainsChild(item.projectid)
        );
      });
    },
    getProjectIds(projectList){
        let ids = [];
        for (let project of projectList){
          ids.push(project.projectid)
        }
        return ids;
    },
        getUserIds(userList){
        let ids = [];
        for (let user of userList){
          ids.push(user.userid)
        }
        return ids;
    },
    setFieldEmptyErrorMessage(name) {
      this.errorMessage = 'Het veld "' + name + '" mag niet leeg zijn.';
    },
    clearForm() {
      this.projectname = "";
      this.projectdescription = "";
      this.userSearchTerm = "";
      this.parentSearchTerm = "";
      this.childSearchTerm = "";

      this.selectedUsers = [];
      this.selectedProjects = [];
      this.selectedChildren = [];
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
    filteredParents: function () {
      if (this.filteredParents.length == 0) {
        document.getElementById("parentDropdown").classList.remove("show");
      } else {
        document.getElementById("parentDropdown").classList.add("show");
      }
    },
    filteredChildren: function () {
      if (this.filteredChildren.length == 0) {
        document.getElementById("childDropdown").classList.remove("show");
      } else {
        document.getElementById("childDropdown").classList.add("show");
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
#childProjectsSearchBar{
    margin-top: 5px;
  margin-bottom: 10px;
}
#selectedUserList {
  font-family: AddeleThin;
}
#selectedParentList {
  font-family: AddeleThin;
}
#selectedChildList{
   font-family: AddeleThin;
}
#errorMessage {
  margin-bottom: 10px;
  color: red;
}
.entryDeleteButton {
  background-color: red;
  border-radius: 5px;
  color: white;
}
</style>
