<template>
  <div class="user-listing">
    <ConfirmDialogue ref="confirmDialogue"></ConfirmDialogue>
    <div class="row">
      <VerticalHeader class="d-block d-lg-none"></VerticalHeader>
      <!-- small screens-->
      <div class="col d-block d-lg-none">
        <div
          class="full-button mobileRow extraLarge"
          @click="onClick()"
        >{{ user.first_name + " " + user.last_name }}</div>
        <div class="mobileRow">{{ user.email }}</div>
        <div class="mobileRow">{{ user.phone_number }}</div>
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
          <select
            v-model="selectedRole"
            :disabled="!canUpdateUserRole()"
            v-if="userIsNotProtected()"
          >
            <option v-for="role in Object.keys(this.roles)" v-bind:key="role">{{ role }}</option>
          </select>
          <div v-else>{{ this.selectedRole }}</div>
        </div>
        <div class="mobileRow">{{ user.amountprojects }}</div>
        <div class="mobileRow">
          <div v-if="userIsNotProtected()">
            <img
              style="cursor: pointer"
              src="@\assets\images\screening1.png"
              v-if="screeningstate == 'Geblokkeerd'"
              @click="
                () => {
                  this.screeningstate = 'Toegestaan';
                }
              "
            />
            <img
              style="cursor: pointer"
              src="@\assets\images\check.png"
              v-if="screeningstate == 'Toegestaan'"
              @click="
                () => {
                  this.screeningstate = 'Geblokkeerd';
                }
              "
            />
          </div>
          <div v-else>
            <img src="@\assets\images\screening1.png" v-if="screeningstate == 'Geblokkeerd'" />
            <img src="@\assets\images\check.png" v-if="screeningstate == 'Toegestaan'" />
          </div>
        </div>
      </div>

      <!-- large screens-->
      <div class="col-3 d-none d-lg-flex align-items-center justify-content-start">
        <router-link
          title="Naar profiel"
          :to="'/user/' + this.user.userid"
          class="name-button"
        >{{ user.first_name + " " + user.last_name }}</router-link>
      </div>
      <div class="col d-none d-lg-flex align-items-center justify-content-center">
        {{
          user.created.toLocaleString("nl-NL", {
            day: "numeric",
            month: "numeric",
            year: "numeric",
          })
        }}
      </div>
      <div class="col d-none d-lg-flex align-items-center justify-content-center">
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
      <div class="col d-none d-lg-flex align-items-center justify-content-center">
        <select v-model="selectedRole" :disabled="!canUpdateUserRole()" v-if="userIsNotProtected()">
          <option v-for="role in Object.keys(this.roles)" v-bind:key="role">{{ role }}</option>
        </select>
        <div v-else>{{ this.selectedRole }}</div>
      </div>
      <div
        class="col d-none d-lg-flex align-items-center justify-content-center"
      >{{ user.amountprojects }}</div>
      <div
        class="col d-none d-lg-flex align-items-center justify-content-center"
        id="screening justify-content-center"
      >
        <div class="iconHolder">
          <div v-if="userIsNotProtected()">
            <img
              style="cursor: pointer"
              src="@\assets\images\screening1.png"
              v-if="screeningstate == 'Geblokkeerd'"
              @click="
                () => {
                  this.screeningstate = 'Toegestaan';
                }
              "
            />
            <img
              style="cursor: pointer"
              src="@\assets\images\check.png"
              v-if="screeningstate == 'Toegestaan'"
              @click="
                () => {
                  this.screeningstate = 'Geblokkeerd';
                }
              "
            />
          </div>
          <div v-else>
            <img src="@\assets\images\screening1.png" v-if="screeningstate == 'Geblokkeerd'" />
            <img src="@\assets\images\check.png" v-if="screeningstate == 'Toegestaan'" />
          </div>
        </div>
      </div>

      <div class="col d-lg-flex align-items-center justify-content-center">
        <span class="button-span-right">
          <UserButtons
            @removeUser="handleRemoveUser(this.user)"
            v-bind:user="this.user"
          ></UserButtons>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import VerticalHeader from "./VerticalHeader.vue";
import UserService from "@/services/UserService.js";
import PermissionService from "@/services/PermissionService.js";
import ConfirmDialogue from "@/shared_components/ConfirmDialogue.vue";
import AlertService from "@/services/AlertService.js";
import UserButtons from "@/pages/manage/users/UserButtons.vue";

export default {
  props: ["user", "all_roles"],
  components: { VerticalHeader, ConfirmDialogue, UserButtons },
  name: "UserListing",
  data: function () {
    return {
      previousRole: this.user.role_name,
      selectedRole: this.user.role_name,
      screeningstates: {
        Geblokkeerd: 0,
        Toegestaan: 1,
      },

      previousScreeningstate: "",
      screeningstate: "",
      roles: {},
    };
  },
  watch: {
    screeningstate: async function (val) {
      if (val != this.previousScreeningstate) {
        let action;
        if (val == "Toegestaan") {
          action = "deblokkeren";
        } else {
          action = "blokkeren";
        }
        const ok = await this.$refs.confirmDialogue.show({
          title: "Toegang veranderen",
          message:
            'Wil je de gebruiker "' +
            this.user.first_name +
            " " +
            this.user.last_name +
            '" echt  ' +
            action +
            "?",
        });
        if (ok) {
          const screeningstateId = this.screeningstates[val];

          UserService.updateUserScreening(screeningstateId, this.user.userid)
            .then((response) => {
              this.previousScreeningstate = val;
              this.$emit(
                "screeningChanged",
                this.user.userid,
                screeningstateId
              );
              AlertService.handleSuccess(response);
            })
            .catch((err) => {
              AlertService.handleError(err);
              this.screeningstate = this.previousScreeningstate;
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
            .then((response) => {
              this.previousRole = this.selectedRole;
              this.$emit("roleChanged", this.user.userid, roleid);
              AlertService.handleSuccess(response);
            })
            .catch((err) => {
              AlertService.handleError(err);
              this.selectedRole = this.previousRole;
            });
        } else {
          this.selectedRole = this.previousRole;
        }
      }
    },
  },
  created() {
    for (const role of this.all_roles) {
      if (role.is_protected != 1) {
        this.roles[role.role_name] = role.roleid;
      }
    }

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
    userIsNotProtected() {
      for (const role of this.all_roles) {
        if (role.roleid == this.user.roleid) {
          return !role.is_protected;
        }
      }
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
          .then((response) => {
            this.$emit("removeUser", user.userid);
            AlertService.handleSuccess(response);
          })
          .catch((err) => {
            AlertService.handleError(err);
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
.name-button {
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
.name-button:hover {
  background-color: var(--blue1);
  color: white;
}

.user-listing {
  box-sizing: border-box;
  color: var(--blue1);
  overflow: visible;
  background-color: rgb(234, 234, 234);
  border-radius: 0 0.2rem 0.2rem 0;
  /* margin-bottom: 0.3rem; */
  font-size: 1.6vh;
  border-bottom: 1px solid #e1e1e1;
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
  border-style: none;
}
.row select {
  background: linear-gradient(
    to bottom right,
    rgba(255, 255, 255, 0.8),
    rgba(225, 225, 225, 0.9)
  );
}

.button-span-right {
  margin-left: auto;
}
</style>