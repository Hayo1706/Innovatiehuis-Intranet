<template>
  <div class="accordion" :id="'accordion' + this.project.projectid">
    <div class="accordion-item">
      <h2 class="accordion-header" id="heading">
        <button
          class="accordion-button collapsed"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="'#collapseDescription' + this.project.projectid"
          aria-expanded="false"
          :aria-controls="'collapseDescription' + this.project.projectid"
        >
          Beschrijving
        </button>
      </h2>
      <div
        :id="'collapseDescription' + this.project.projectid"
        class="accordion-collapse collapse"
        aria-labelledby="heading"
      >
        <div class="accordion-body">
          {{ project.description }}
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header" id="heading">
        <button
          class="accordion-button collapsed"
          :id="'collapseMembersButton' + this.project.projectid"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="'#collapseMembers' + this.project.projectid"
          aria-expanded="false"
          :aria-controls="'collapseMembers' + this.project.projectid"
          @click="this.onMembersClick()"
        >
          Leden
        </button>
      </h2>
      <div
        :id="'collapseMembers' + this.project.projectid"
        class="accordion-collapse collapse"
        aria-labelledby="heading"
      >
        <div class="accordion-body">
          <form autocomplete="off">
            <SearchBar
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

          <div
            class="full-button"
            v-for="member in this.members"
            v-bind:key="member.userid"
            @click="navigateUser(member.userid)"
          >
            {{ member.first_name }} {{ member.last_name }}
          </div>
          <div v-if="this.members.length == 0">Geen resultaten</div>
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header" id="heading">
        <button
          class="accordion-button collapsed"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="'#collapseParents' + this.project.projectid"
          aria-expanded="false"
          :aria-controls="'collapseParents' + this.project.projectid"
          :id="'collapseParentsButton' + this.project.projectid"
          @click="this.onParentsClick()"
        >
          Overkoepelende projecten
        </button>
      </h2>
      <div
        :id="'collapseParents' + this.project.projectid"
        class="accordion-collapse collapse"
        aria-labelledby="heading"
      >
        <div class="accordion-body">
          <div
            class="full-button"
            v-for="parent in this.parents"
            v-bind:key="parent.projectid"
            @click="navigate(parent.projectid)"
          >
            {{ parent.project_name }}
          </div>
          <div v-if="this.parents.length == 0">Geen resultaten</div>
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header" id="heading">
        <button
          class="accordion-button collapsed"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="'#collapseChildren' + this.project.projectid"
          aria-expanded="false"
          :aria-controls="'collapseChildren' + this.project.projectid"
          :id="'collapseChildrenButton' + this.project.projectid"
          @click="this.onChildrenClick()"
        >
          Sub-projecten
        </button>
      </h2>
      <div
        :id="'collapseChildren' + this.project.projectid"
        class="accordion-collapse collapse"
        aria-labelledby="heading"
      >
        <div class="accordion-body">
          <div
            class="full-button"
            v-for="child in this.children"
            v-bind:key="child.projectid"
            @click="navigate(child.projectid)"
          >
            {{ child.project_name }}
          </div>
          <div v-if="this.children.length == 0">Geen resultaten</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ProjectService from "@/services/ProjectService.js";
import UserService from "@/services/UserService.js";
import SearchBar from "@/shared_components/SearchBar.vue";
export default {
  props: ["project"],
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

      memberToAdd: null,
      userSearchTerm: "",
      users: [],
      filteredUsers: [],
      projects: [],
    };
  },
  methods: {
    getUserIds(userList) {
      let ids = [];
      for (let user of userList) {
        ids.push(user.userid);
      }
      return ids;
    },
    selectUser(user) {
      this.memberToAdd = user;
      this.userSearchTerm = "";
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
    onParentsClick() {
      if (this.accordeonIsOpen("collapseParentsButton")) {
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
      }
      this.parentsOpen = !this.parentsOpen;
    },
    onChildrenClick() {
      if (this.accordeonIsOpen("collapseChildrenButton")) {
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
      }
      this.childrenOpen = !this.childrenOpen;
    },
    onMembersClick() {
      if (this.accordeonIsOpen("collapseMembersButton")) {
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
    accordeonIsOpen(idName) {
      return (
        document
          .getElementById(idName + this.project.projectid)
          .attributes.getNamedItem("aria-expanded").value == "true"
      );
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
          .classList.toggle("show");
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
}

.addButton {
  background-color: var(--gold1);
  border-color: var(--blue1);
  display: inline;
  color: white;
  margin-top: 10px;
  margin-bottom: 20px;
  margin-left: 10px;
}

.searchbar {
  width: 50%;
  margin-bottom: 10px;
}
</style>
