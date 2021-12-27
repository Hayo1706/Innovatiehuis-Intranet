<template>
  <div id="user-listing">
    <div class="row">
      <VerticalHeader class="d-block d-lg-none"></VerticalHeader>
      <!-- small screens-->
      <div class="col d-block d-lg-none">
        <div class="userButton mobileRow" @click="onClick()">
          {{ user.firstname + " " + user.lastname }}
        </div>
        <div class="mobileRow">
          {{
            user.createdat.toLocaleString("nl-NL", {
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
          {{
            user.lastseen.toLocaleString("nl-NL", {
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
          <select v-model="selectedRole">
            <option v-for="role in Object.keys(this.roles)" v-bind:key="role">
              {{ role }}
            </option>
          </select>
        </div>
        <div class="mobileRow">{{ user.amountprojects }}</div>
        <div class="mobileRow">
          <select v-model="screeningstate">
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
        <div class="userButton">{{ user.firstname + " " + user.lastname }}</div>
      </div>
      <div class="col d-none d-lg-block">
        {{
          user.createdat.toLocaleString("nl-NL", {
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
        {{
          user.lastseen.toLocaleString("nl-NL", {
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
        <select v-model="selectedRole">
          <option v-for="role in Object.keys(this.roles)" v-bind:key="role">
            {{ role }}
          </option>
        </select>
      </div>
      <div class="col d-none d-lg-block">{{ user.amountprojects }}</div>
      <div class="col d-none d-lg-block">
        <select v-model="screeningstate">
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
        <a class="link" @click="handleRemoveUser(this.user)">Verwijderen</a>
      </div>
    </div>
  </div>
</template>

<script>
import VerticalHeader from "./VerticalHeader.vue";
import UserService from "@/services/UserService.js";
export default {
  props: ["user"],
  components: { VerticalHeader },
  name: "UserListing",
  data: function () {
    return {
      previousRole: this.user.rolename,
      selectedRole: this.user.rolename,
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
          'Wil je de screeningstatus van de gebruiker "' +
            this.user.firstname +
            " " +
            this.user.lastname +
            '" echt veranderen naar "' +
            val +
            '"?'
        );
        if (answer) {
          const screeningstateId = this.screeningstates[val];

          UserService.updateUser(
            {
              firstname: this.user.firstname,
              lastname: this.user.lastname,
              email: this.user.email,
              roleid: this.user.roleid,
              screeningstatus: screeningstateId,
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
            this.user.firstname +
            " " +
            this.user.lastname +
            '" echt veranderen naar ' +
            val +
            "?"
        );
        if (answer) {
          const roleid = this.roles[val];

          UserService.updateUser(
            {
              firstname: this.user.firstname,
              lastname: this.user.lastname,
              email: this.user.email,
              roleid: roleid,
              screeningstatus: this.user.screeningstatus,
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
      this.user.screeningstatus
    );
    this.screeningstate = this.getKeyByValue(
      this.screeningstates,
      this.user.screeningstatus
    );
  },
  methods: {
    onClick() {
      this.$router.push("/user/" + this.user.userid);
    },
    async handleRemoveUser(user) {
      let answer = confirm(
        'Wil je het project  de gebruiker "' +
          user.firstname +
          " " +
          user.lastname +
          " echt verwijderen ?"
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
  background-color: var(--blue3);
  margin: 3px;
  padding: 10px;
  box-sizing: border-box;
  color: var(--blue1);
  font-family: AddeleSemiBold;
}
.row {
  padding-top: 12px;
}
.userButton {
  font-weight: bold;
  background-color: var(--gold2);
  color: var(--blue1);
  border-style: outset;
  border-radius: 8px;
  padding-left: 10px;
  padding-right: 10px;
  height: fit-content;
  cursor: pointer;
  width: fit-content;
}
.mobileRow {
  min-height: 53px;
}
img {
  width: 50px;
  margin-right: 2px;
  margin-top: 10px;
}
.link {
  cursor: pointer;
  color: var(--gold2);
  display: block;
  margin-bottom: 10px;
  text-decoration: none;
}
select {
  border-radius: 0.25rem;
}
</style>