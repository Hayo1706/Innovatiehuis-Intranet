<template>
  <div class="accordion" :id="'accordion' + project.projectid">
    <div class="accordion-item">
      <h2 class="accordion-header" id="heading">
        <button
          ref="btn"
          :id="'collapseDetailsButton' + this.project.projectid"
          class="accordion-button collapsed"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="'#collapseName' + this.project.projectid"
          aria-expanded="false"
          :aria-controls="'collapseName' + this.project.projectid"
          @click="openDetails()"
          :disabled="disabled"
        >
          Details
        </button>
      </h2>
      <div
        :id="'collapseName' + this.project.projectid"
        class="accordion-collapse collapse"
        aria-labelledby="heading"
      >
        <div v-if="canUpdateProject()" class="accordion-body">
          Naam:
          <textarea class="area form-control" v-model="projectname" />
          <button class="addButton" @click="updateNameDescription()">
            Wijzigen
          </button>
          <br />
          Beschrijving:
          <textarea class="area form-control" v-model="projectdescription" />
          <button class="addButton" @click="updateNameDescription()">
            Wijzigen
          </button>
          <br />
          Leden toevoegen:
          <form autocomplete="off">
            <SearchBar
              v-show="canUpdateProject()"
              v-bind:searchTerm="this.userSearchTerm"
              :id="'searchUsersBar' + this.project.projectid"
              autocomplete="off"
              class="searchbar"
              @searchBarChanged="
                (searchTerm) => {
                  handleSearchUser(searchTerm);
                }
              "
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
          <div v-if="memberToAdd">
            {{ this.memberToAdd.first_name }} {{ this.memberToAdd.last_name }}
            <button
              @click="addUser()"
              class="btn pmd-btn-fab pmd-ripple-effect btn-primary addButton"
            >
              toevoegen
            </button>
          </div>

          <div v-for="member in this.members" v-bind:key="member.userid">
            <span class="full-button" @click="navigateUser(member.userid)">
              {{ member.first_name }} {{ member.last_name }}
            </span>
            <button
              class="userDeleteButton"
              v-show="canUpdateProject()"
              @click="removeUser(member.userid)"
            >
              x
            </button>
          </div>

          <div v-if="this.members.length == 0" class="text">
            Geen resultaten
          </div>
          <br />
          Overkoepelende projecten toevoegen:
          <form autocomplete="off">
            <SearchBar
              v-show="canUpdateProject()"
              v-bind:searchTerm="this.parentSearchTerm"
              :id="'searchParentsBar' + this.project.projectid"
              autocomplete="off"
              class="searchbar"
              @searchBarChanged="
                (searchTerm) => {
                  handleSearchParent(searchTerm);
                }
              "
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
          <div v-if="parentToAdd">
            {{ this.parentToAdd.project_name }}
            <button
              @click="addParent()"
              class="btn pmd-btn-fab pmd-ripple-effect btn-primary addButton"
            >
              toevoegen
            </button>
          </div>

          <div v-for="parent in this.parents" v-bind:key="parent.projectid">
            <span
              class="full-button"
              @click="navigateProject(parent.projectid)"
            >
              {{ parent.project_name }}
            </span>
            <button
              class="userDeleteButton"
              v-show="canUpdateProject()"
              @click="removeParent(parent.projectid)"
            >
              x
            </button>
          </div>
          <div v-if="this.parents.length == 0" class="text">
            Geen resultaten
          </div>
          <br />
          Sub-projecten toevoegen:
          <form autocomplete="off">
            <SearchBar
              v-show="canUpdateProject()"
              v-bind:searchTerm="this.childSearchTerm"
              :id="'searchParentsBar' + this.project.projectid"
              autocomplete="off"
              class="searchbar"
              @searchBarChanged="
                (searchTerm) => {
                  handleSearchChild(searchTerm);
                }
              "
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
          <div v-if="childToAdd">
            {{ this.childToAdd.project_name }}
            <button
              @click="addChild()"
              class="btn pmd-btn-fab pmd-ripple-effect btn-primary addButton"
            >
              toevoegen
            </button>
          </div>

          <div v-for="child in this.children" v-bind:key="child.projectid">
            <span class="full-button" @click="navigateProject(child.projectid)">
              {{ child.project_name }}
            </span>
            <button
              class="userDeleteButton"
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
        <div v-else class="accordion-body">
          Naam:
          <br />
          <span class="text">{{ project.project_name }}</span>
          <br />
          <br />
          beschrijving:
          <br />
          <span class="text">{{ project.description }}</span>
          <br />
          <br />
          Leden:
          <form autocomplete="off">
            <SearchBar
              v-show="canUpdateProject()"
              v-bind:searchTerm="this.userSearchTerm"
              :id="'searchUsersBar' + this.project.projectid"
              autocomplete="off"
              class="searchbar"
              @searchBarChanged="
                (searchTerm) => {
                  handleSearchUser(searchTerm);
                }
              "
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
          <div v-if="memberToAdd">
            {{ this.memberToAdd.first_name }} {{ this.memberToAdd.last_name }}
            <button
              @click="addUser()"
              class="btn pmd-btn-fab pmd-ripple-effect btn-primary addButton"
            >
              toevoegen
            </button>
          </div>

          <div v-for="member in this.members" v-bind:key="member.userid">
            <span class="full-button" @click="navigateUser(member.userid)">
              {{ member.first_name }} {{ member.last_name }}
            </span>
            <button
              class="userDeleteButton"
              v-show="canUpdateProject()"
              @click="removeUser(member.userid)"
            >
              x
            </button>
          </div>

          <div v-if="this.members.length == 0" class="text">
            Geen resultaten
          </div>
          <br />
          Overkoepelende projecten:
          <form autocomplete="off">
            <SearchBar
              v-show="canUpdateProject()"
              v-bind:searchTerm="this.parentSearchTerm"
              :id="'searchParentsBar' + this.project.projectid"
              autocomplete="off"
              class="searchbar"
              @searchBarChanged="
                (searchTerm) => {
                  handleSearchParent(searchTerm);
                }
              "
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
          <div v-if="parentToAdd">
            {{ this.parentToAdd.project_name }}
            <button
              @click="addParent()"
              class="btn pmd-btn-fab pmd-ripple-effect btn-primary addButton"
            >
              toevoegen
            </button>
          </div>

          <div v-for="parent in this.parents" v-bind:key="parent.projectid">
            <span
              class="full-button"
              @click="navigateProject(parent.projectid)"
            >
              {{ parent.project_name }}
            </span>
            <button
              class="userDeleteButton"
              v-show="canUpdateProject()"
              @click="removeParent(parent.projectid)"
            >
              x
            </button>
          </div>
          <div v-if="this.parents.length == 0" class="text">
            Geen resultaten
          </div>
          <br />
          Sub-projecten:
          <form autocomplete="off">
            <SearchBar
              v-show="canUpdateProject()"
              v-bind:searchTerm="this.childSearchTerm"
              :id="'searchParentsBar' + this.project.projectid"
              autocomplete="off"
              class="searchbar"
              @searchBarChanged="
                (searchTerm) => {
                  handleSearchChild(searchTerm);
                }
              "
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
          <div v-if="childToAdd">
            {{ this.childToAdd.project_name }}
            <button
              @click="addChild()"
              class="btn pmd-btn-fab pmd-ripple-effect btn-primary addButton"
            >
              toevoegen
            </button>
          </div>

          <div v-for="child in this.children" v-bind:key="child.projectid">
            <span class="full-button" @click="navigateProject(child.projectid)">
              {{ child.project_name }}
            </span>
            <button
              class="userDeleteButton"
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
      </div>
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
    };
  },
  mounted() {
    if (this.open) {
      this.$nextTick(() => {
        setTimeout(() => {
          this.$refs.btn.click();
          this.disabled = true;
          document.getElementById(
            "collapseDetailsButton" + this.project.projectid
          ).textContent = "";
        }, 500);
      });
    }
  },
  methods: {
    updateNameDescription() {
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
          alert("Er ging wat mis, probeer later opnieuw");
        });
    },
    selectUser(user) {
      this.memberToAdd = user;
      this.userSearchTerm = "";
    },
    selectParent(project) {
      this.parentToAdd = project;
      this.parentSearchTerm = "";
    },
    selectChild(project) {
      this.childToAdd = project;
      this.childSearchTerm = "";
    },
    addUser() {
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
    addParent() {
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
    addChild() {
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
    membersContainsUser(userid) {
      for (const user of this.members) {
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
          !this.membersContainsUser(item.userid)
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
    parentsContainsProject(projectid) {
      for (const parent of this.parents) {
        if (parent.projectid == projectid) {
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
          !this.childrenContainsProject(item.projectid) &&
          item.projectid != this.project.projectid
        );
      });
    },
    childrenContainsProject(projectid) {
      for (const child of this.children) {
        if (child.projectid == projectid) {
          return true;
        }
      }
      return false;
    },
    getFilteredParents() {
      return this.projects.filter((item) => {
        return (
          item.project_name
            .toLowerCase()
            .includes(this.parentSearchTerm.toLowerCase()) &&
          !this.parentsContainsProject(item.projectid) &&
          item.projectid != this.project.projectid
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

      this.onMembersClick();
      this.onParentsClick();
      this.onChildrenClick();
    },
    onParentsClick() {
      if (this.accordeonIsOpen("collapseDetailsButton")) {
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
    onChildrenClick() {
      if (this.accordeonIsOpen("collapseDetailsButton")) {
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
    onMembersClick() {
      if (this.accordeonIsOpen("collapseDetailsButton")) {
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
      PermissionService;

      return (
        PermissionService.userHasPermission("may_update_any_project") ||
        PermissionService.userHasPermission("may_update_own_project")
      );
    },
    accordeonIsOpen(idName) {
      return (
        document
          .getElementById(idName + this.project.projectid)
          .attributes.getNamedItem("aria-expanded").value == "true"
      );
    },
    refreshAllAcordeons() {
      var arr = document.getElementsByClassName("accordion-button");

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
.accordion {
  margin-top: 30px;
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
.userDeleteButton {
  background-color: red;
  border-radius: 5px;
  color: white;
}
.text {
  font-family: AddeleThin;
}
</style>
