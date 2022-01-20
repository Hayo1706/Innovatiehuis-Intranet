<template>
  <div class="component-container">
    <div class="component-header">Persoonsgegevens</div>
      <div class="component-body-white overflow">
        <table>
          <td  v-for="(rolevalue, rolekey) in roles"  v-bind:key="rolevalue">
            <tr  v-for="(values, keys) in rolevalue" v-bind:key="values">
              <td class="roles-row">
                <input class="roles-row" type="checkbox" v-model="this.roles[rolekey][keys]" :true-value="1" :false-value="0">
              </td>
            </tr>
          </td>
        </table>
      </div>
  </div>
</template>

<script>
import UserService from "@/services/UserService";

export default {
  name: "AccesControlView",
  data: function () {
    return {
      roles: '',
    };
  },
  created() {
    UserService.getRoles().then((response) => {
      console.log(response)
      response.forEach(role => {
        delete role.role_name
        delete role.roleid
      });
      this.roles = response
    })
    .catch((err) => {
      if (err.response) {
        console.log(err.response.status);
      }
    });
  },
  methods: {
    getRoles(){
      console.log(1)
      console.log(this.roles)
      return this.roles
    },
  },
}
</script>

<style scoped>
.overflow{
  overflow: scroll;
}
.roles-row{
  padding: 10px;
}
</style>