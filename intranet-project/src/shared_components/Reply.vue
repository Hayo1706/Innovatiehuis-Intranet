<template>
  <div id="comment">
    <p>{{ this.content }}</p>
    <p>{{ this.username }} ({{ this.timestamp.toLocaleDateString() }})
  </div>
</template>

<script>
// import ProjectService from "@/services/ProjectService.js";
export default {
  name: "Reply",
  props: {
    id: { type: Number, required: true },
    announcementid: { type: Number, required: true },
    userid: { type: Number, required: true },
    username: { type: String, required: true },
    content: { type: String, required: true },
    timestamp: { type: Date, required: true }
  },
  data: function () {
    return {

    };
  },
  methods: {
    // remove() {
    //   ProjectService.removeReply(this.id)
    //   .then((response) => {
    //     ALERT WEET JE HET ZEKER?
    //     console.log(response);
    //   })
    //   .catch((err) => {
    //     if (err.response) {
    //       console.log(err.response.status);
    //     }
    //     alert(err);
    //   });

    //   this.$emit("reload");
    // },
  },
};
</script>

<style scoped>
#reply {
  width: 100%;
  background-color: var(--gold3);
}
</style>