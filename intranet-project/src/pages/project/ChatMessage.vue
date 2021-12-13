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
    name: { type: String, required: true },
    message: { type: String, required: true },
  },
  data: function () {
    return {
    };
  },
};
</script>