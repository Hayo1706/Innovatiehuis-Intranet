<template>
    <div class="accordion-item">
        <h2 class="accordion-header" :id="'heading' + this.id">
            <button class="accordion-button" type="button" data-bs-toggle="collapse" :data-bs-target="'#collapse' + this.id" aria-expanded="false" aria-controls="panelsStayOpen-collapseOne">
                {{ this.date.toLocaleString('nl-NL', { day: 'numeric', month: 'long' }) }}: {{ this.title }}
            </button>
        </h2>
        <div :id="'collapse' + this.id" class="accordion-collapse collapse show" :aria-labelledby="'heading' + this.id">
            <div class="accordion-body">
                <strong><router-link :to="'/user/' + this.id">{{ this.username }}</router-link></strong> ({{this.date.toLocaleDateString()}}) <br>
                {{ this.content }}
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: "Announcement",
  props: {
    id: {
        type: Number,
        required: true
    },
    date: {
        type: Date,
        required: true
    },
    userid: {
        type: Number,
        required: true
    },
    username: {
        type: String,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    content: {
        type: String,
        required: true
    },
  },
  data: function () {
    return {
        
    };
  },
}
</script>

<style scoped>
.accordion-button {
    background-color: var(--blue2);
    color: white;
}
</style>