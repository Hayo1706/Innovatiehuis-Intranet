<template>
  <div id="user-listing">
    <ConfirmDialogue ref="confirmDialogue"></ConfirmDialogue>
    <div class="row">
      <VerticalHeader class="d-block d-lg-none"></VerticalHeader>
      <!-- small screens-->
      <div class="col d-block d-lg-none">
        <div class="full-button mobileRow extraLarge" @click="onClick()">
          {{ user.first_name + " " + user.last_name }}
        </div>
        <div class="mobileRow">
          {{
            user.created.toLocaleString("nl-NL", {
              day: "numeric",
              month: "numeric",
              year: "numeric",
            })
          }}
        </div>
        <div class="mobileRow">
          {{
            user.last_seen.toLocaleString("nl-NL", {
              day: "numeric",
              month: "numeric",
              year: "numeric",
              hour: "numeric",
              minute: "numeric",
              second: "numeric",
            })
          }}
        </div>
        <div class="mobileRow">
          <select v-model="selectedRole" :disabled="!canUpdateUserRole()">
            <option v-for="role in Object.keys(this.roles)" v-bind:key="role">
              {{ role }}
            </option>
          </select>
        </div>
        <div class="mobileRow">{{ user.amountprojects }}</div>
        <div class="mobileRow">
          <div class="dropdown">
            <button
              class="btn dropdown-toggle"
              type="button"
              id="dropdownMenuButton1"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <img
                src="@\assets\images\screening1.png"
                v-if="screeningstate == 'nog niet in behandeling'"
              />
              <img
                src="@\assets\images\screening2.png"
                v-if="screeningstate == 'in behandeling'"
              />
              <img
                src="@\assets\images\check.png"
                v-if="screeningstate == 'voltooid'"
              />
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
              <select
                class="dropdown-item"
                v-model="screeningstate"
                :disabled="!canUpdateUserScreening()"
              >
                <option
                  v-for="screeningstate in Object.keys(this.screeningstates)"
                  v-bind:key="screeningstate"
                >
                  {{ screeningstate }}
                </option>
              </select>
            </ul>
          </div>
        </div>
      </div>

      <!-- large screens-->
      <div
        class="col-3 d-none d-lg-flex align-items-center justify-content-start"
        @click="onClick()"
      >
        <div class="name-button">
          {{ user.first_name + " " + user.last_name }}
        </div>
      </div>
      <div
        class="col d-none d-lg-flex align-items-center justify-content-center"
      >
        {{
          user.created.toLocaleString("nl-NL", {
            day: "numeric",
            month: "numeric",
            year: "numeric",
          })
        }}
      </div>
      <div
        class="col d-none d-lg-flex align-items-center justify-content-center"
      >
        {{
          user.last_seen.toLocaleString("nl-NL", {
            day: "numeric",
            month: "numeric",
            year: "numeric",
            hour: "numeric",
            minute: "numeric",
            second: "numeric",
          })
        }}
      </div>
      <div
        class="col d-none d-lg-flex align-items-center justify-content-center"
      >
        <select v-model="selectedRole" :disabled="!canUpdateUserRole()">
          <option v-for="role in Object.keys(this.roles)" v-bind:key="role">
            {{ role }}
          </option>
        </select>
      </div>
      <div
        class="col d-none d-lg-flex align-items-center justify-content-center"
      >
        {{ user.amountprojects }}
      </div>
      <div
        class="col d-none d-lg-flex align-items-center justify-content-center"
        id="screening justify-content-center"
      >
        <div class="listing-icon iconHolder">
          <div class="dropdown">
            <button
              class="btn dropdown-toggle"
              type="button"
              id="dropdownMenuButton1"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <img
                src="@\assets\images\screening1.png"
                v-if="screeningstate == 'nog niet in behandeling'"
              />
              <img
                src="@\assets\images\screening2.png"
                v-if="screeningstate == 'in behandeling'"
              />
              <img
                src="@\assets\images\check.png"
                v-if="screeningstate == 'voltooid'"
              />
            </button>
            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
              <select
                class="dropdown-item"
                v-model="screeningstate"
                :disabled="!canUpdateUserScreening()"
              >
                <option
                  v-for="screeningstate in Object.keys(this.screeningstates)"
                  v-bind:key="screeningstate"
                >
                  {{ screeningstate }}
                </option>
              </select>
            </ul>
          </div>
        </div>
      </div>

      <div class="col d-lg-flex align-items-center justify-content-center">
        <a @click="handleRemoveUser(this.user)" v-show="canDelete()"
          ><div class="listing-icon iconHolder">
            <img src="@\assets\images\delete.png" /></div
        ></a>
      </div>
    </div>
  </div>
</template>

<script>
import VerticalHeader from "./VerticalHeader.vue";
import UserService from "@/services/UserService.js";
import PermissionService from "@/services/PermissionService.js";
import ConfirmDialogue from "@/shared_components/ConfirmDialogue.vue";
export default {
  props: ["user"],
  components: { VerticalHeader, ConfirmDialogue },
  name: "UserListing",
  data: function () {
    return {
      previousRole: this.user.role_name,
      selectedRole: this.user.role_name,
      roles: { observer: 1, student: 2, moderator: 3, admin: 4 },
      screeningstates: {
        "nog niet in behandeling": 0,
        "in behandeling": 1,
        voltooid: 2,
      },

      previousScreeningstate: "",
      screeningstate: "",
    };
  },
  watch: {
    screeningstate: async function (val) {
      if (val != this.previousScreeningstate) {
        const ok = await this.$refs.confirmDialogue.show({
          title: "Screening veranderen",
          message:
            'Wil je de screening status van de gebruiker "' +
            this.user.first_name +
            " " +
            this.user.last_name +
            '" echt veranderen naar "' +
            val +
            '"?',
        });
        if (ok) {
          const screeningstateId = this.screeningstates[val];

          UserService.updateUserScreening(screeningstateId, this.user.userid)
            .then(() => {
              this.previousScreeningstate = val;
              this.$emit(
                "screeningChanged",
                this.user.userid,
                screeningstateId
              );
              return;
            })
            .catch(() => {
              this.screeningstate = this.previousScreeningstate;
              alert("Er ging iets mis!");
            });
        } else {
          this.screeningstate = this.previousScreeningstate;
        }
      }
    },
    selectedRole: async function (val) {
      if (val != this.previousRole) {
        const ok = await this.$refs.confirmDialogue.show({
          title: "Rol veranderen",
          message:
            'Wil je de rol van de gebruiker "' +
            this.user.first_name +
            " " +
            this.user.last_name +
            '" echt veranderen naar ' +
            val +
            "?",
        });
        if (ok) {
          const roleid = this.roles[val];

          UserService.updateUserRole(roleid, this.user.userid)
            .then(() => {
              this.previousRole = this.selectedRole;
              this.$emit("roleChanged", this.user.userid, roleid);
              return;
            })
            .catch(() => {
              this.selectedRole = this.previousRole;
              alert("Er ging iets mis!");
            });
        } else {
          this.selectedRole = this.previousRole;
        }
      }
    },
  },
  created() {
    this.previousScreeningstate = this.getKeyByValue(
      this.screeningstates,
      this.user.screening_status
    );
    this.screeningstate = this.getKeyByValue(
      this.screeningstates,
      this.user.screening_status
    );
  },
  methods: {
    canDelete() {
      return (
        PermissionService.userHasPermission("may_delete_any_user") &&
        this.user.userid != localStorage.getItem("userid")
      );
    },
    canUpdateUserRole() {
      return (
        PermissionService.userHasPermission("may_update_any_user_role") &&
        this.user.userid != localStorage.getItem("userid")
      );
    },
    canUpdateUserScreening() {
      return (
        PermissionService.userHasPermission(
          "may_update_any_user_screening_status"
        ) && this.user.userid != localStorage.getItem("userid")
      );
    },
    onClick() {
      this.$router.push("/user/" + this.user.userid);
    },
    async handleRemoveUser(user) {
      const ok = await this.$refs.confirmDialogue.show({
        title: "Verwijderen",
        message:
          'Wil je de gebruiker "' +
          user.first_name +
          " " +
          user.last_name +
          '" echt verwijderen ?',
      });

      if (ok) {
        UserService.deleteUser(user.userid)
          .then(() => {
            this.$emit("removeUser", user.userid);
          })
          .catch((err) => {
            if (err.response) {
              console.log(err.response.status);
            }
          });
      }
    },
    getKeyByValue(object, value) {
      return Object.keys(object).find((key) => object[key] == value);
    },
  },
};
</script>

<style scoped>
.name-button{
  border-radius: 0.5rem;
  background-color: var(--blue2);
  width: 100%;
  height: 100%;
  align-items: center;
  display: flex;
  cursor: pointer;
  font-size: 14pt;
  color: white;
  padding: 6px;
  text-decoration: none;
}
.name-button:hover{
  background-color: var(--blue1);
  color: white;
}

#user-listing {
  box-sizing: border-box;
  color: var(--blue1);
  overflow: visible;
  background: linear-gradient(
    to right top,
    rgba(230, 230, 230, 0.7),
    rgba(230, 230, 230, 0.9)
  );
  border-radius: 0.5rem;
  margin-bottom: 0.3rem;
  font-size: 1.6vh;
  border: solid var(--gold4) 2px;
}
.userButton {
  font-weight: bold;
  background-color: var(--gold1);
  color: var(--blue1);
  border-radius: 1rem;
  padding-left: 10px;
  padding-right: 10px;
  height: fit-content;
  cursor: pointer;
  width: fit-content;
  margin-left: 10px;
}
.mobileRow {
  min-height: 50px;
}
.extraLarge {
  height: 70px;
}
img {
  height: 40px;
}
.link {
  cursor: pointer;
  color: var(--gold1);
  display: block;
  margin-bottom: 10px;
  text-decoration: none;
}
select {
  border-radius: 0.25rem;
  width: fit-content;
}
.dropdown-toggle {
  padding: 0px;
  margin: 0px;
}
.dropdown-item {
  margin-right: 10px;
  margin-left: 10px;
}
.iconHolder {
  border-radius: 10%;
}
</style>