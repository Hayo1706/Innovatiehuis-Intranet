<template>
    <div>
        <div class="row">
            {{ this.message }}
        </div>
    </div>
</template>

<script>
export default {
  name: "ChatMessage",
  props: {
    userid: { type: Number, required: true },
    first_name: { type: String, required: true },
    last_name: { type: String, required: true },
    content: { type: String, required: true },
  },
  data: function () {
    return {
    };
  },
};
</script>