<template>
  <div id="userlisting">
    <span>{{ name }}</span>
    <span>{{ created }}</span>
    <span>{{ lastModified }}</span>
    <span>{{ parentUser }}</span>
    <span>{{ subuserCount }}</span>

    <span>
      <img src=".\..\..\..\assets\images\users_icon.png" />
      <img
        @click="archive(this.id)"
        v-if="isArchived"
        src="https://cdn-icons-png.flaticon.com/512/60/60723.png"
      /><img
        @click="archive(this.id)"
        v-else
        src="https://www.pngkey.com/png/full/876-8761970_download-button-comments-icon-png-archive-icon.png"
      />

      <img
        @click="delete_user(this.id)"
        src="https://www.pngrepo.com/png/320601/512/crossed-pistols.png"
      />
    </span>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "UserListing",
  props: [
    "id",
    "name",
    "created",
    "lastModified",
    "role",
    "projects",
    "screening",
  ],
  data: function () {
    return {};
  },
  methods: {
    archive(id) {
      axios
        .put("http://94.212.125.203:5000/api/user/" + id)
        .then(() => {
          this.$emit("reload");
        })
        .catch((error) => {
          console.log(error);
          alert("Something went wrong!");
        });
    },
    delete_user(id) {
      axios
        .delete("http://94.212.125.203:5000/api/user/" + id)
        .then(() => {
          this.$emit("reload");
        })
        .catch((error) => {
          console.log(error);
          alert("Something went wrong!");
        });
    },
  },
};
</script>

<style scoped>
#userlisting {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  color: black;
  flex-basis: 100%;
  gap: 60px;
}

span {
  flex: 1 1 0;
  width: 0;
  overflow-wrap: anywhere;
}
img {
  height: 5vh;
  padding-right: 20px;
  cursor: pointer;
}
</style>