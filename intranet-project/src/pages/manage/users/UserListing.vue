<template>
  <div id="user-listing">
    <div class="row">
      <VerticalHeader class="d-block d-lg-none"></VerticalHeader>
      <!-- small screens-->
      <div class="col d-block d-lg-none">
        <div class="full-button mobileRow" @click="onClick()">
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
          <select
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
          <br />
          <img
            src="@\assets\images\exclamation.png"
            v-if="screeningstate == 'nog niet in behandeling'"
          />
          <img
            src="@\assets\images\waiting.png"
            v-if="screeningstate == 'in behandeling'"
          />
          <img
            src="@\assets\images\check.png"
            v-if="screeningstate == 'voltooid'"
          />
        </div>
      </div>

      <!-- large screens-->
      <div class="col d-none d-lg-block" @click="onClick()">
        <div class="full-button">
          {{ user.first_name + " " + user.last_name }}
        </div>
      </div>
      <div class="col d-none d-lg-block">
        {{
          user.created.toLocaleString("nl-NL", {
            day: "numeric",
            month: "numeric",
            year: "numeric",
          })
        }}
      </div>
      <div class="col d-none d-lg-block">
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
      <div class="col d-none d-lg-block">
        <select v-model="selectedRole" :disabled="!canUpdateUserRole()">
          <option v-for="role in Object.keys(this.roles)" v-bind:key="role">
            {{ role }}
          </option>
        </select>
      </div>
      <div class="col d-none d-lg-block">{{ user.amountprojects }}</div>
      <div class="col d-none d-lg-block" id="screening">
        <select v-model="screeningstate" :disabled="!canUpdateUserScreening()">
          <option
            v-for="screeningstate in Object.keys(this.screeningstates)"
            v-bind:key="screeningstate"
          >
            {{ screeningstate }}
          </option>
        </select>
        <br />
        <img
          src="@\assets\images\exclamation.png"
          v-if="screeningstate == 'nog niet in behandeling'"
        />
        <img
          src="@\assets\images\waiting.png"
          v-if="screeningstate == 'in behandeling'"
        />
        <img
          src="@\assets\images\check.png"
          v-if="screeningstate == 'voltooid'"
        />
      </div>

      <div class="col">
        <a
          class="full-button"
          @click="handleRemoveUser(this.user)"
          v-show="canDelete()"
          >Verwijderen</a
        >
      </div>
    </div>
  </div>
</template>

<script>
import VerticalHeader from "./VerticalHeader.vue";
import UserService from "@/services/UserService.js";
import PermissionService from "@/services/PermissionService.js";
export default {
  props: ["user"],
  components: { VerticalHeader },
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
    screeningstate: function (val) {
      if (val != this.previousScreeningstate) {
        let answer = confirm(
          'Wil je de screening status van de gebruiker "' +
            this.user.first_name +
            " " +
            this.user.last_name +
            '" echt veranderen naar "' +
            val +
            '"?'
        );
        if (answer) {
          const screeningstateId = this.screeningstates[val];

          UserService.updateUser(
            {
              first_name: this.user.first_name,
              last_name: this.user.last_name,
              email: this.user.email,
              roleid: this.user.roleid,
              screening_status: screeningstateId,
            },
            this.user.userid
          )
            .then(() => {
              this.previousRole = this.selectedRole;
              return;
            })
            .catch(() => {
              this.selectedRole = this.previousRole;
              alert("Er ging iets mis!");
            });
        }
      }
    },
    selectedRole: function (val) {
      if (val != this.previousRole) {
        let answer = confirm(
          'Wil je de rol van de gebruiker "' +
            this.user.first_name +
            " " +
            this.user.last_name +
            '" echt veranderen naar ' +
            val +
            "?"
        );
        if (answer) {
          const roleid = this.roles[val];

          UserService.updateUser(
            {
              first_name: this.user.first_name,
              last_name: this.user.last_name,
              email: this.user.email,
              roleid: roleid,
              screening_status: this.user.screening_status,
            },
            this.user.userid
          )
            .then(() => {
              this.previousRole = this.selectedRole;
              return;
            })
            .catch(() => {
              this.selectedRole = this.previousRole;
              alert("Er ging iets mis!");
            });
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
      return PermissionService.userHasPermission("may_delete_any_user");
    },
    canUpdateUserRole() {
      return PermissionService.userHasPermission("may_update_any_user_role");
    },
    canUpdateUserScreening() {
      return PermissionService.userHasPermission(
        "may_update_any_user_screening_status"
      );
    },
    onClick() {
      this.$router.push("/user/" + this.user.userid);
    },
    async handleRemoveUser(user) {
      let answer = confirm(
        'Wil je de gebruiker "' +
          user.first_name +
          " " +
          user.last_name +
          '" echt verwijderen ?'
      );
      if (answer) {
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
#user-listing {
  padding: 10px;
  box-sizing: border-box;
  color: var(--blue1);
  overflow: visible;
  background: linear-gradient(
    to right top,
    rgba(230, 230, 230, 0.7),
    rgba(230, 230, 230, 0.9)
  );
  border-radius: 1rem;
  margin-bottom: 1vh;
  font-size: 1.7vh;
  border: solid var(--gold1) 2px;
}

.row {
  padding-top: 12px;
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
img {
  width: 30px;
  margin-right: 2px;
  margin-top: 10px;
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
}
.full-button {
  width: fit-content;
}
</style>