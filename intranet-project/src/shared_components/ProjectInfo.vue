<template>
  <div class="component-body-white">
    Naam:
    <textarea
      v-if="canUpdateProject()"
      oninput="this.style.height = ''; this.style.height = this.scrollHeight + 'px'"
      onclick="this.style.height = ''; this.style.height = this.scrollHeight + 'px'"
      class="area form-control"
      v-model="projectname"
    />
    <div v-else class="text">
      {{ projectname }}
    </div>
    <br />Beschrijving:
    <textarea
      v-if="canUpdateProject()"
      oninput="this.style.height = ''; this.style.height = this.scrollHeight + 'px'"
      onclick="this.style.height = ''; this.style.height = this.scrollHeight + 'px'"
      class="area form-control"
      v-model="projectdescription"
    />
    <div v-else class="text">
      {{ projectdescription }}
    </div>
    <br />
    <div class="container-fluid">
      <div class="row">
        <div class="col">
          Leden:
          <div v-for="member in this.members" v-bind:key="member.userid">
            <span class="full-button" @click="navigateUser(member.userid)"
              >{{ member.first_name }} {{ member.last_name }}</span
            >
            <button
              class="deleteButton"
              v-show="canUpdateProject()"
              @click="removeUser(member.userid)"
            >
              x
            </button>
            <br />
          </div>

          <div v-if="this.members.length == 0" class="text">
            Geen resultaten
          </div>
        </div>
        <div class="col">
          Overkoepelende projecten:
          <div v-for="parent in this.parents" v-bind:key="parent.projectid">
            <span
              class="full-button"
              @click="navigateProject(parent.projectid)"
              >{{ parent.project_name }}</span
            >
            <button
              class="deleteButton"
              v-show="canUpdateProject()"
              @click="removeParent(parent.projectid)"
            >
              x
            </button>
          </div>
          <div v-if="this.parents.length == 0" class="text">
            Geen resultaten
          </div>
        </div>
        <div class="col">
          Sub-projecten:
          <div v-for="child in this.children" v-bind:key="child.projectid">
            <span
              class="full-button"
              @click="navigateProject(child.projectid)"
              >{{ child.project_name }}</span
            >
            <button
              class="deleteButton"
              v-show="canUpdateProject()"
              @click="removeChild(child.projectid)"
            >
              x
            </button>
          </div>
          <div v-if="this.children.length == 0" class="text">
            Geen resultaten
          </div>
        </div>
        <div class="col"></div>
        <div class="col"></div>
      </div>
    </div>

    <div v-show="canUpdateProject()">
      <br />
      Leden toevoegen:
      <br />
      <form autocomplete="off">
        <SearchBar
          placeholder="Zoek gebruikers..."
          :id="'searchUsersBar' + this.project.projectid"
          autocomplete="off"
          class="searchbar"
          @searchBarChanged="
            (searchTerm) => {
              handleSearchUser(searchTerm);
            }
          "
          v-bind:searchTerm="this.userSearchTerm"
        ></SearchBar>
      </form>
      <div
        class="dropdown-menu"
        :id="'userSearchDropdown' + this.project.projectid"
      >
        <div
          class="dropdown-item"
          v-for="user in filteredUsers"
          v-bind:key="user.userid"
          @click="selectUser(user)"
        >
          {{ user.first_name }} {{ user.last_name }}
        </div>
      </div>
      <div v-if="this.selectedUsers.length != 0">
        <span
          class="text"
          v-for="user in this.selectedUsers"
          v-bind:key="user.userid"
        >
          {{ user.first_name }} {{ user.last_name }}
          <button
            class="deleteButton"
            v-show="canUpdateProject()"
            @click="removeSelectedUser(user.userid)"
          >
            x</button
          >,&nbsp;</span
        >
        <br />
        <br />
      </div>
    </div>
    <div v-show="canUpdateProject()">
      Overkoepelende projecten toevoegen:
      <br />
      <form autocomplete="off">
        <SearchBar
          v-show="canUpdateProject()"
          placeholder="Zoek projecten"
          :id="'searchParentsBar' + this.project.projectid"
          autocomplete="off"
          class="searchbar"
          @searchBarChanged="
            (searchTerm) => {
              handleSearchParent(searchTerm);
            }
          "
          v-bind:searchTerm="this.parentSearchTerm"
        ></SearchBar>
      </form>
      <div
        class="dropdown-menu"
        :id="'parentSearchDropdown' + this.project.projectid"
      >
        <div
          class="dropdown-item"
          v-for="parent in filteredParents"
          v-bind:key="parent.projectid"
          @click="selectParent(parent)"
        >
          {{ parent.project_name }}
        </div>
      </div>
      <div v-if="this.selectedParents.length != 0">
        <span
          class="text"
          v-for="parent in this.selectedParents"
          v-bind:key="parent.projectid"
        >
          {{ parent.project_name }}
          <button
            class="deleteButton"
            v-show="canUpdateProject()"
            @click="removeSelectedParent(parent.projectid)"
          >
            x</button
          >,&nbsp;</span
        >
        <br />
        <br />
      </div>
    </div>
    <div v-show="canUpdateProject()">
      Sub-projecten toevoegen:
      <br />
      <form autocomplete="off">
        <SearchBar
          v-show="canUpdateProject()"
          placeholder="Zoek projecten..."
          :id="'searchParentsBar' + this.project.projectid"
          autocomplete="off"
          class="searchbar"
          @searchBarChanged="
            (searchTerm) => {
              handleSearchChild(searchTerm);
            }
          "
          v-bind:searchTerm="this.childSearchTerm"
        ></SearchBar>
      </form>
      <div
        class="dropdown-menu"
        :id="'childSearchDropdown' + this.project.projectid"
      >
        <div
          class="dropdown-item"
          v-for="child in filteredChildren"
          v-bind:key="child.projectid"
          @click="selectChild(child)"
        >
          {{ child.project_name }}
        </div>
      </div>
      <div v-if="this.selectedChildren.length != 0">
        <span
          class="text"
          v-for="child in this.selectedChildren"
          v-bind:key="child.projectid"
        >
          {{ child.project_name }}
          <button
            class="deleteButton"
            v-show="canUpdateProject()"
            @click="removeSelectedChild(child.projectid)"
          >
            x</button
          >,&nbsp;</span
        >
        <br />
      </div>

      <br />
      <button class="addButton" @click="updateProjectDetails()">
        Wijzigingen opslaan
      </button>
    </div>
  </div>
</template>

<script>
import ProjectService from "@/services/ProjectService.js";
import UserService from "@/services/UserService.js";
import SearchBar from "@/shared_components/SearchBar.vue";
import PermissionService from "@/services/PermissionService.js";
export default {
  props: ["project", "open"],
  components: { SearchBar },
  name: "ProjectInfo",
  data: function () {
    return {
      parents: [],
      children: [],
      members: [],
      parentsOpen: false,
      childrenOpen: false,
      membersOpen: false,
      projectname: "",
      projectdescription: "",
      memberToAdd: null,
      userSearchTerm: "",
      users: [],
      filteredUsers: [],
      projects: [],

      parentToAdd: null,
      parentSearchTerm: "",
      filteredParents: [],

      childToAdd: null,
      childSearchTerm: "",
      filteredChildren: [],
      disabled: false,

      selectedUsers: [],
      selectedParents: [],
      selectedChildren: [],
    };
  },
  mounted() {
    if (this.open) {
      setTimeout(() => {
        this.openDetails();
      }, 500);
    }
  },
  methods: {
    updateProjectDetails() {
      const project = {
        project_name: this.projectname,
        description: this.projectdescription,
      };
      ProjectService.updateProjectNameDescription(
        this.project.projectid,
        project
      )
        .then(() => {
          this.$emit("nameOrDescriptionChanged", project);
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
          }
          alert("Er ging iets mis, probeer later opnieuw");
        });
    },
    selectUser(user) {
      this.selectedUsers.push(user);
      this.userSearchTerm = "";
    },
    selectParent(project) {
      this.selectedParents.push(project);
      this.parentSearchTerm = "";
    },
    selectChild(project) {
      this.selectedChildren.push(project);
      this.childSearchTerm = "";
    },
    removeSelectedParent(id) {
      this.selectedParents = this.selectedParents.filter((project) => {
        return project.projectid != id;
      });
    },
    removeSelectedChild(id) {
      this.selectedChildren = this.selectedChildren.filter((project) => {
        return project.projectid != id;
      });
    },
    removeSelectedUser(id) {
      this.selectedUsers = this.selectedUsers.filter((user) => {
        return user.userid != id;
      });
    },
    addUsers() {
      UserService.addUserToProject(
        this.project.projectid,
        this.memberToAdd.userid
      )
        .then(() => {
          this.memberToAdd = null;
          this.loadMembers();
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
          }
          alert("Er ging wat mis, probeer later opnieuw");
        });
    },
    addParents() {
      ProjectService.addParentToProject(
        this.project.projectid,
        this.parentToAdd.projectid
      )
        .then(() => {
          this.refreshAllAcordeons();
          this.parentToAdd = null;
          this.loadParents();
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
          }
          alert("Er ging wat mis, probeer later opnieuw");
        });
    },
    addChildren() {
      ProjectService.addChildToProject(
        this.project.projectid,
        this.childToAdd.projectid
      )
        .then(() => {
          this.refreshAllAcordeons();
          this.childToAdd = null;
          this.loadChildren();
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
          }
          alert("Er ging wat mis, probeer later opnieuw");
        });
    },
    removeChild(childid) {
      ProjectService.removeChildFromProject(this.project.projectid, childid)
        .then(() => {
          this.refreshAllAcordeons();
          this.loadChildren();
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
          }
          alert("Er ging wat mis, probeer later opnieuw");
        });
    },
    removeParent(parentid) {
      ProjectService.removeParentFromProject(this.project.projectid, parentid)
        .then(() => {
          this.refreshAllAcordeons();
          this.loadParents();
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
          }
          alert("Er ging wat mis, probeer later opnieuw");
        });
    },
    removeUser(userid) {
      UserService.removeUserFromProject(this.project.projectid, userid)
        .then(() => {
          this.loadMembers();
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
          }
          alert("Er ging wat mis, probeer later opnieuw");
        });
    },
    userListContainsUser(userList, userid) {
      for (const user of userList) {
        if (user.userid == userid) {
          return true;
        }
      }
      return false;
    },
    getFilteredUsers() {
      return this.users.filter((item) => {
        return (
          (item.first_name + " " + item.last_name)
            .toLowerCase()
            .includes(this.userSearchTerm.toLowerCase()) &&
          !this.userListContainsUser(this.members, item.userid) &&
          !this.userListContainsUser(this.selectedUsers, item.userid)
        );
      });
    },
    handleSearchUser(name) {
      if (name) {
        this.userSearchTerm = name;
        this.filteredUsers = this.getFilteredUsers();
      } else {
        this.filteredUsers = [];
      }
    },
    projectListContainsProject(projectList, projectid) {
      for (const project of projectList) {
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
    handleSearchChild(name) {
      if (name) {
        this.childSearchTerm = name;
        this.filteredChildren = this.getFilteredChildren();
      } else {
        this.filteredChildren = [];
      }
    },
    getFilteredChildren() {
      return this.projects.filter((item) => {
        return (
          item.project_name
            .toLowerCase()
            .includes(this.childSearchTerm.toLowerCase()) &&
          !this.projectListContainsProject(this.children, item.projectid) &&
          item.projectid != this.project.projectid &&
          !this.projectListContainsProject(
            this.selectedChildren,
            item.projectid
          )
        );
      });
    },
    getFilteredParents() {
      return this.projects.filter((item) => {
        return (
          item.project_name
            .toLowerCase()
            .includes(this.parentSearchTerm.toLowerCase()) &&
          !this.projectListContainsProject(this.parents, item.projectid) &&
          item.projectid != this.project.projectid &&
          !this.projectListContainsProject(this.selectedParents, item.projectid)
        );
      });
    },
    loadParents() {
      ProjectService.getParentsById(this.project.projectid)
        .then((response) => {
          //remove the project from the view
          this.parents = response;
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    openDetails() {
      this.projectdescription = this.project.description;
      this.projectname = this.project.project_name;

      this.handleMembersLoading();
      this.handleParentsLoading();
      this.handleChildrenLoading();
    },
    handleParentsLoading() {
      if (this.accordeonIsOpen()) {
        this.loadParents();
        ProjectService.getProjects()
          .then((response) => {
            this.projects = response;
          })
          .catch((err) => {
            if (err.response) {
              console.log(err.response.status);
            }
          });
      } else {
        this.parentToAdd = null;
        this.parentSearchTerm = "";
      }
    },
    loadChildren() {
      ProjectService.getChildrenById(this.project.projectid)
        .then((response) => {
          //remove the project from the view
          this.children = response;
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    handleChildrenLoading() {
      if (this.accordeonIsOpen()) {
        this.loadChildren();
        ProjectService.getProjects()
          .then((response) => {
            this.projects = response;
          })
          .catch((err) => {
            if (err.response) {
              console.log(err.response.status);
            }
          });
      } else {
        this.childToAdd = null;
        this.childSearchTerm = "";
      }
    },
    handleMembersLoading() {
      if (this.accordeonIsOpen()) {
        this.loadMembers();

        UserService.getUsers()
          .then((response) => {
            this.users = response;
          })
          .catch((err) => {
            if (err.response) {
              console.log(err.response.status);
            }
          });
      } else {
        this.memberToAdd = null;
        this.userSearchTerm = "";
      }
    },
    loadMembers() {
      UserService.getUsersByProject(this.project.projectid)
        .then((response) => {
          //remove the project from the view
          this.members = response;
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },

    navigate(projectid) {
      this.$router.push("/project/" + projectid);
    },
    navigateUser(userid) {
      this.$router.push("/user/" + userid);
    },
    navigateProject(projectid) {
      this.$router.push("/project/" + projectid);
    },
    canUpdateProject() {
      return (
        PermissionService.userHasPermission("may_update_any_project") ||
        PermissionService.userHasPermission("may_update_own_project")
      );
    },
    accordeonIsOpen() {
      return this.open;
    },
    refreshAllAcordeons() {
      var arr = document.getElementsByClassName("accordion_button");

      for (let j = 0; j < arr.length; j++) {
        if (
          !arr[j]
            .getAttribute("aria-controls")
            .includes(this.project.projectid.toString()) &&
          !arr[j].classList.contains("collapsed")
        ) {
          arr[j].click();
          setTimeout(() => {
            arr[j].click();
          }, 500);
        }
      }
    },
  },

  watch: {
    open: function () {
      if (this.open) {
        this.openDetails();
      }
    },
    filteredUsers: function () {
      if (this.filteredUsers.length == 0) {
        document
          .getElementById("userSearchDropdown" + this.project.projectid)
          .classList.remove("show");
      } else {
        document
          .getElementById("userSearchDropdown" + this.project.projectid)
          .classList.add("show");
      }
    },
    filteredParents: function () {
      if (this.filteredParents.length == 0) {
        document
          .getElementById("parentSearchDropdown" + this.project.projectid)
          .classList.remove("show");
      } else {
        document
          .getElementById("parentSearchDropdown" + this.project.projectid)
          .classList.add("show");
      }
    },
    filteredChildren: function () {
      if (this.filteredChildren.length == 0) {
        document
          .getElementById("childSearchDropdown" + this.project.projectid)
          .classList.remove("show");
      } else {
        document
          .getElementById("childSearchDropdown" + this.project.projectid)
          .classList.add("show");
      }
    },
  },
};
</script>


<style scoped>
.accordion-item {
  background-color: rgba(255, 255, 255, 0.7);
  border: none;
}
.accordion-button {
  border: none;
  height: 2rem;
  background: var(--blue4);
  text-align: center;
  padding: 0px 1vw;
}
.accordion-item:first-of-type .accordion-button {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
.accordion-button:hover {
  background: var(--blue3);
}
button {
  font-family: Montserrat;
  color: var(--blue1);
}
.full-button {
  width: fit-content;
  display: inline-block;
  margin-bottom: 5px;
}

.addButton {
  background-color: var(--gold1);
  border-color: var(--blue1);
  display: inline;
  color: white;
  margin-top: 10px;
  margin-bottom: 20px;
  margin-left: 10px;

  border-radius: 1rem;
  margin: 5px;
  align-items: center;
  display: flex;
  cursor: pointer;
  font-size: 14pt;
  color: white;
  padding: 6px;
  text-decoration: none;
}

.area {
  width: 70%;
  display: block;
  font-family: AddeleThin;
}

.searchbar {
  width: 50%;
  margin-bottom: 10px;
}
.deleteButton {
  background-color: red;
  border-radius: 5px;
  color: white;
}
.text {
  font-family: AddeleThin;
}
.container-fluid {
  margin: 0px;
  max-width: 10000px;
  padding: 0;
}
</style>
