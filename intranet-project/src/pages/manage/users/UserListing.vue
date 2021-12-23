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
        <div class="mobileRow"></div>
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
      <div class="col d-none d-lg-block"></div>

      <div class="col"></div>
    </div>
  </div>
</template>

<script>
import VerticalHeader from "./VerticalHeader.vue";
export default {
  props: ["user"],
  components: { VerticalHeader },
  name: "UserListing",
  data: function () {
    return {
      previousRole: this.user.rolename,
      selectedRole: this.user.rolename,
      roles: { observer: 1, student: 2, moderator: 3, admin: 4 },
    };
  },
  watch: {
    selectedRole: function (val) {
      if (val != this.previousRole) {
        let answer = confirm(
          'Wil je de rol van "' +
            this.user.firstname +
            " " +
            this.user.lastname +
            '" echt veranderen naar ' +
            val +
            "?"
        );
        if (answer) {
          this.previousRole = this.selectedRole;

          const roleid = this.roles[val];
          console.log(roleid);
          const updatedOnBackend = true;
          //TODO update the role on the backend

          if (updatedOnBackend) {
            return;
          } else {
            //display error
          }
        }
        //on failure of updating on backend or cancel by user, undo setting a new role
        this.selectedRole = this.previousRole;
      }
    },
  },
  methods: {
    onClick() {
      this.$router.push("/user/" + this.user.userid);
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
  font-family: AddeleSemiBold;
}
.mobileRow {
  height: 53px;
}
</style>