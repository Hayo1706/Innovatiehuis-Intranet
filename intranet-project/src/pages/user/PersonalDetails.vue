<template>
    <div class="component-container">
      <p>Personal Details</p>
      <UserListing v-bind:user="this.user"/>
    </div>

</template>

<script>
import UserListing from "@/pages/manage/users/UserListing";
import UserService from "@/services/UserService";
export default {
  name: "PersonalDetails",
  components: {UserListing},
  props: [

  ],
  data: function () {
    return {
      user: "",
    };
  },
  async created() {
    UserService.getUserById(1)
        .then((response) => {
          this.user = response;
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
  },
}
</script>


<style scoped>
p {
  color: white;
  font-size: calc(2vw + 2vh);
  height: 100%;
  width: 500px;
  margin: 0;
  text-align: center;
  background-color: var(--blue4);
  border-style: outset;
  }
</style>