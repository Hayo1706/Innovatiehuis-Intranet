<template>
  <div class="component-body-white">
    Naam:
    <input
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
            <button
              class="deleteButton"
              v-show="canUpdateProject()"
              @click="removeUserFromList(member.userid)"
            >
              x
            </button>
            <button class="member-item" @click="navigateUser(member.userid)">
              {{ member.first_name }} {{ member.last_name }}
            </button>
            <br />
          </div>

          <div v-if="this.members.length == 0" class="text">
            Geen
          </div>
        </div>
        <div class="col">
          Overkoepelende projecten:
          <div v-for="parent in this.parents" v-bind:key="parent.projectid">
            <button
              class="deleteButton"
              v-show="canUpdateProject()"
              @click="removeProjectFromList('parents', parent.projectid)"
            >
              x
            </button>
            <button
              class="member-item"
              @click="navigateProject(parent.projectid)"
            >
              {{ parent.project_name }}
            </button>
          </div>
          <div v-if="this.parents.length == 0" class="text">
            Geen
          </div>
        </div>
        <div class="col">
          Sub-projecten:
          <div v-for="child in this.children" v-bind:key="child.projectid">
            <button
              class="deleteButton"
              v-show="canUpdateProject()"
              @click="removeProjectFromList('children', child.projectid)"
            >
              x
            </button>
            <button
              class="member-item"
              @click="navigateProject(child.projectid)"
            >
              {{ child.project_name }}
            </button>
          </div>
          <div v-if="this.children.length == 0" class="text">
            Geen
          </div>
        </div>
      </div>
    </div>

    <div class="row" v-show="canUpdateProject()">
      <div class="col">
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
      </div>
      <div class="col">
        <br />
        Overkoepelende projecten toevoegen:
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
      </div>
      <div class="col">
        <br />
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
      </div>
    </div>

    <br />
    <button
      v-if="this.changes"
      id="save-button"
      class="full-button"
      @click="updateProjectDetails()"
    >
      Wijzigingen opslaan
    </button>
  </div>
</template>

<script>
import ProjectService from "@/services/ProjectService.js";
import UserService from "@/services/UserService.js";
import SearchBar from "@/shared_components/SearchBar.vue";
import PermissionService from "@/services/PermissionService.js";
import AlertService from "@/services/AlertService.js";
export default {
  props: ["project", "open"],
  components: { SearchBar },
  name: "ProjectInfo",
  data: function () {
    return {
      parents: [],
      children: [],
      members: [],

      projectname: "",
      projectdescription: "",

      new_projectname: false,
      new_projectdescription: false,

      userSearchTerm: "",
      filteredUsers: [],

      users: [],
      projects: [],

      parentSearchTerm: "",
      filteredParents: [],

      childSearchTerm: "",
      filteredChildren: [],
      disabled: false,

      changes: false,
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
      let all_ok = true;
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

          ProjectService.updateMembersOfProject(this.project.projectid, {
            ids: this.getUserIds(this.members),
          })
            .then(() => {
              ProjectService.updateParentsOfProject(this.project.projectid, {
                ids: this.getProjectIds(this.parents),
              })
                .then(() => {
                  ProjectService.updateChildrenOfProject(
                    this.project.projectid,
                    {
                      ids: this.getProjectIds(this.children),
                    }
                  )
                    .then(() => {
                      if (all_ok) {
                        AlertService.alert(
                          "De wijzigingen zijn opgeslagen!",
                          "success"
                        );
                        this.changes = false;
                        this.refreshAllAcordeons();
                      } else {
                        this.openDetails();
                        this.refreshAllAcordeons();
                      }
                    })
                    .catch((err) => {
                      console.log(err);
                      //invalid operation on server
                      if (err.response) {
                        console.log(err.response.status);
                      }
                      AlertService.handleError(err);
                      all_ok = false;
                    });
                })
                .catch((err) => {
                  console.log(err);
                  //invalid operation on server
                  if (err.response) {
                    console.log(err.response.status);
                  }
                  AlertService.handleError(err);
                  all_ok = false;
                });
            })
            .catch((err) => {
              console.log(err);
              //invalid operation on server
              if (err.response) {
                console.log(err.response.status);
              }
              AlertService.handleError(err);
              all_ok = false;
            });
        })
        .catch((err) => {
          //invalid operation on server
          if (err.response) {
            console.log(err.response.status);
          }
          AlertService.handleError(err);
          all_ok = false;
        });
    },
    selectUser(user) {
      this.members.push(user);
      this.changes = true;
      this.userSearchTerm = "";
    },
    selectParent(project) {
      this.parents.push(project);
      this.changes = true;
      this.parentSearchTerm = "";
    },
    selectChild(project) {
      this.children.push(project);
      this.changes = true;
      this.childSearchTerm = "";
    },
    removeProjectFromList(list, id) {
      if (list == "parents") {
        this.changes = true;
        this.parents = this.parents.filter((project) => {
          return project.projectid != id;
        });
        if (this.filteredParents.length != 0)
          this.filteredParents = this.getFilteredParents();
      } else if (list == "children") {
        this.changes = true;
        this.children = this.children.filter((project) => {
          return project.projectid != id;
        });
        if (this.filteredChildren.length != 0)
          this.filteredChildren = this.getFilteredChildren();
      } else {
        throw new Error("Unsupported operation");
      }
    },
    removeUserFromList(id) {
      this.members = this.members.filter((user) => {
        return user.userid != id;
      });
      this.changes = true;
      if (this.filteredUsers.length != 0)
        this.filteredUsers = this.getFilteredUsers();
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
          !this.userListContainsUser(this.members, item.userid)
        );
      });
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
          item.projectid != this.project.projectid
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
          item.projectid != this.project.projectid
        );
      });
    },
    loadParents() {
      ProjectService.getParentsById(this.project.projectid)
        .then((response) => {
          this.parents = response.data.result;
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
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
        this.parentSearchTerm = "";
        this.loadParents();
        if (localStorage.getItem("may_read_any_project") == 1) {
          ProjectService.getProjects()
            .then((response) => {
              this.projects = response.data.result;
              AlertService.handleSuccess(response);
            })
            .catch((err) => {
              AlertService.handleError(err);
            });
        }
      } else {
        this.parentSearchTerm = "";
      }
    },
    loadChildren() {
      ProjectService.getChildrenById(this.project.projectid)
        .then((response) => {
          this.children = response.data.result;
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
        });
    },
    handleChildrenLoading() {
      if (this.accordeonIsOpen()) {
        this.childSearchTerm = "";
        this.loadChildren();
      } else {
        this.childSearchTerm = "";
      }
    },
    handleMembersLoading() {
      if (this.accordeonIsOpen()) {
        this.userSearchTerm = "";
        this.loadMembers();
        if (localStorage.getItem("may_read_any_project") == 1) {
          UserService.getUsers()
            .then((response) => {
              this.users = response.data.result;
              AlertService.handleSuccess(response);
            })
            .catch((err) => {
              AlertService.handleError(err);
            });
        }
      } else {
        this.userSearchTerm = "";
      }
    },
    loadMembers() {
      UserService.getUsersByProject(this.project.projectid)
        .then((response) => {
          this.members = response.data.result;
          AlertService.handleSuccess(response);
        })
        .catch((err) => {
          AlertService.handleError(err);
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
        PermissionService.userHasPermission("may_update_any_project") &&
        PermissionService.userHasPermission("may_read_any_project")
      );
    },
    accordeonIsOpen() {
      return this.open;
    },
    getProjectIds(projectList) {
      let ids = [];
      for (let project of projectList) {
        ids.push(project.projectid);
      }
      return ids;
    },
    getUserIds(userList) {
      let ids = [];
      for (let user of userList) {
        ids.push(user.userid);
      }
      return ids;
    },
  },

  watch: {
    projectname: function () {
      if (this.new_projectname) {
        this.changes = true;
      } else {
        this.new_projectname = true;
      }
    },
    projectdescription: function () {
      if (this.new_projectdescription) {
        this.changes = true;
      } else {
        this.new_projectdescription = true;
      }
    },
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
.member-item {
  background-color: rgb(239, 239, 239);
  width: fit-content;
  height: fit-content;
  border-radius: 0 5px 5px 0;
  border-left-width: 0px;
  border-color: #d4d4d4;
  border-style: solid;
  cursor: pointer;
  margin-bottom: 5px;
  font-size: 14pt;
  max-width: 80%;
}
.member-item:hover {
  background-color: rgb(231, 231, 231);
}

#save-button {
  display: inline;
  color: white;
  align-items: center;
  margin-left: auto;
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
  background-color: #ff0808cf;
  border-color: #d4d4d4;
  border-radius: 5px 0 0 5px;
  border: 2px 0 2px 2px solid grey;
  border-style: solid;
  border-right-width: 0;
  color: white;
  font-size: 14pt;
  width: 2.5ch;
}
.text {
  font-family: AddeleThin;
  font-size: 16pt;
}
.container-fluid {
  margin: 0px;
  max-width: 10000px;
  padding: 0;
}
</style>
