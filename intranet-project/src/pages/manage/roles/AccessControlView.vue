<template>
  <div class="component-container" style="max-width: 1200px; margin: auto">
    <div class="component-header">Rollenoverzicht
      <img src="../../../assets/images/add_icon.png"
        class="component-header-button"
           data-bs-toggle="modal"
           data-bs-target="#roleModal"
           v-if="canCrudRoles"
      >

    </div>
      <div class="component-body-white">

        <ul class="nav nav-tabs nav-justified">
          <li class="nav-item" v-for="(rolevalue) in roles" v-bind:key="rolevalue.role_name">
            <a class="nav-link" @click.prevent="setActive(rolevalue.role_name)" :class="{ active: isActive(rolevalue.role_name) }" :href="'#'+ rolevalue.role_name">{{ rolevalue.role_name}}</a>
          </li>
        </ul>
        <div class="tab-content py-3" id="myTabContent">
          <div class="tab-pane fade" v-for="(rolevalue, rolekey) in roles" v-bind:key="rolevalue.role_name" :class="{ 'active show': isActive(rolevalue.role_name) }" :id="rolevalue.role_name">
            <hr v-if="canCrudRoles && rolevalue.role_name !== 'admin'">
            <div style="height: 40px;
            margin: auto;
            max-width: 500px;
             display: flex;
             justify-content: space-around;
             align-items: center;"
             v-if="canCrudRoles && rolevalue.role_name !== 'admin'">
              
              <div>
              <img src="../../../assets/images/lock-icon-11.png" style="height: 40px;"/>
              <label class="switch">

                <input
                    id="hidearchivedcheckbox"
                    type="checkbox"
                    name="hidearchivedcheckbox"
                    v-model="uneditable"
                />
                <span class="slider round"></span>
              </label>
              </div>
              <img src="../../../assets/images/delete_red.png"
                   style="height: 40px; width: auto"
                   class="component-header-button"
                    @click="selectDelete(rolevalue.roleid,rolevalue.role_name)"
                   data-bs-toggle="modal"
                   data-bs-target="#confirmModal"
              >
              <button class="full-button"
                      style="max-width: 10vw;margin: 0;height: 100%"
                      @click="selectSave(rolevalue, rolevalue.roleid)"
                      :disabled="uneditable"
                      data-bs-toggle="modal"
                      data-bs-target="#confirmModal"
              >
                Opslaan
              </button>
            </div>
            <hr v-if="canCrudRoles && rolevalue.role_name !== 'admin'">
            <table style="margin: auto" >
              <tr>
                <td style="padding-right: 10vw">power_level</td>
                <td style="padding-right: 10vw"/>
                <td v-if="excludedPerms(keys)">
                  <input type="number" v-model="this.roles[rolekey]['power_level']" :disabled="rolevalue.role_name === 'admin' ? true : uneditable">
                </td>
              </tr>
              <tr>
                <td style="padding-right: 10vw">may_cud_users_with_power_level_up_to</td>
                <td style="padding-right: 10vw"/>
                <td v-if="excludedPerms(keys)">
                  <input type="number" v-model="this.roles[rolekey]['may_cud_users_with_power_level_up_to']" :disabled="rolevalue.role_name === 'admin' ? true : uneditable">
                </td>
              </tr>
              <tr v-for="(values, keys) in rolevalue" v-bind:key="keys">
                  <td  v-if="excludedPerms(keys)" style="padding-right: 10vw">
                    {{keys}}
                  </td>
                  <td  v-if="excludedPerms(keys)" style="padding-right: 10vw">
                    {{ values === 1 ? 'True' : 'False' }}

                  </td>
                  <td v-if="excludedPerms(keys)">
                    <input type="checkbox" v-model="this.roles[rolekey][keys]" :disabled="rolevalue.role_name === 'admin' ? true : uneditable" :true-value="1" :false-value="0">
                  </td>
              </tr>

            </table>
          </div>
        </div>
      </div>
  </div>

  <!-- Modal -->
  <div
      class="modal fade"
      id="roleModal"
      tabindex="-1"
      aria-labelledby="roleModalLabel"
      aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="roleModalLabel">
            Nieuwe rol toevoegen
          </h5>
          <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <input
              type="text"
              class="form-control"
              id="title-text"
              placeholder="Rolnaam"
              v-model="this.newRole"
          />
        </div>
        <div class="modal-footer">
          <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
          >
            Annuleren
          </button>
          <button
              type="button"
              class="btn btn-primary"
              data-bs-dismiss="modal"
              @click="addRole()"
          >
            Bevestigen
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Confirmation Modal -->
  <div
      class="modal fade"
      id="confirmModal"
      aria-hidden="true"
      ref="modal"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 v-if="selectedDeleteId !== ''" class="modal-title">
            {{this.selectedDeleteName.charAt(0).toUpperCase() + this.selectedDeleteName.slice(1)}} verwijderen?
          </h5>
          <h5 v-else class="modal-title">
             Wijzigingen opslaan?
          </h5>
          <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <label>Wachtwoord:</label>
          <input
              type="text"
              style="font-family: disks;margin-top: 10px"
              autocomplete="new-password"
              class="form-control"
              ref="password"
          />
        </div>
        <div class="modal-footer">
          <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
          >
            Annuleren
          </button>
          <button
              type="button"
              class="btn btn-primary"
              data-bs-dismiss="modal"
              @click="selectedDeleteName !== '' ? deleteRole() : saveConfiguration()"
              value="a"
          >
            Bevestigen
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserService from "@/services/UserService";
import AlertService from "@/services/AlertService";
import PermissionService from "@/services/PermissionService";

export default {
  name: "AccessControlView",
  data: function () {
    return {
      roles: '',
      activeItem: 'student',
      uneditable: true,
      newRole: "",
      selectedDeleteId: '',
      selectedDeleteName: '',
      selectedRole: '',
      selectedId: '',
    };
  },
  created() {
    this.refreshRoles()
  },
  methods: {
    getRoles(){
      return this.roles
    },
    excludedPerms(perm){
      return !(perm === 'role_name' || perm === 'roleid'
          || perm === 'power_level' || perm === 'may_cud_users_with_power_level_up_to')
    },
    selectDelete(id,name){
      this.selectedDeleteId = id;
      this.selectedDeleteName = name;
      this.selectedRole = '';
      this.selectedId = '';
    },
    selectSave(role, id){
      this.selectedDeleteId = '';
      this.selectedDeleteName = '';
      this.selectedRole = role;
      this.selectedId = id;
    },
    isActive (menuItem) {
      return this.activeItem === menuItem
    },
    setActive (menuItem) {
      this.activeItem = menuItem
    },
    canCrudRoles(){
      return PermissionService.userHasPermission('may_crud_roles')
    },
    saveConfiguration(){
      this.selectedRole['password'] = this.$refs.password.value
      this.$refs.password.value = null
      UserService.updateRole(this.selectedRole,this.selectedId).then((response) => {
        AlertService.handleSuccess(response)
      })
      .catch((err) => {
        AlertService.handleError(err);
      });
      this.$refs.password.value = null

    },
    addRole(){
      UserService.addRole({'role_name': this.newRole}).then((response) => {
        this.refreshRoles();
        this.newRole = ''
        AlertService.handleSuccess(response)
      }).catch((err) => {
          AlertService.handleError(err);
      });

    },
    deleteRole(){
      UserService.deleteRole(this.selectedDeleteId, this.$refs.password.value).then((response) => {
        this.refreshRoles();
        if (this.activeItem == this.selectedDeleteName){
          this.activeItem = 'admin'
        }
        AlertService.handleSuccess(response)
      }).catch((err) => {
        AlertService.handleError(err);
      });
      this.$refs.password.value = null

    },
    refreshRoles(){
      UserService.getRoles().then((response) => {
        this.roles = response.data.result;
        AlertService.handleSuccess(response);
      }).catch((err) => {
        if (err.response) {
          AlertService.handleError(err);
        }
      });
    }

  },
}
</script>

<style scoped>
.switch {
  position: relative;
  display: inline-block;
  margin-left: 1em;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: var(--blue2);
}

input:focus + .slider {
  box-shadow: 0 0 1px var(--blue2);
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>