<template>
  <div class="accordion" :id="'accordion' + this.project.projectid">
    <div class="accordion-item">
      <h2 class="accordion-header" id="heading">
        <button
          class="accordion-button collapsed"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="'#collapseDescription' + this.project.projectid"
          aria-expanded="false"
          :aria-controls="'collapseDescription' + this.project.projectid"
        >
          Beschrijving
        </button>
      </h2>
      <div
        :id="'collapseDescription' + this.project.projectid"
        class="accordion-collapse collapse"
        aria-labelledby="heading"
      >
        <div class="accordion-body">
          {{ project.description }}
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header" id="heading">
        <button
          class="accordion-button collapsed"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="'#collapseParents' + this.project.projectid"
          aria-expanded="false"
          :aria-controls="'collapseParents' + this.project.projectid"
        >
          Overkoepelende projecten
        </button>
      </h2>
      <div
        :id="'collapseParents' + this.project.projectid"
        class="accordion-collapse collapse"
        aria-labelledby="heading"
      >
        <div class="accordion-body">
          {{ project.description }}
        </div>
      </div>
    </div>

    <div class="accordion-item">
      <h2 class="accordion-header" id="heading">
        <button
          class="accordion-button collapsed"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="'#collapseChildren' + this.project.projectid"
          aria-expanded="false"
          :aria-controls="'collapseChildren' + this.project.projectid"
        >
          Sub-projecten
        </button>
      </h2>
      <div
        :id="'collapseChildren' + this.project.projectid"
        class="accordion-collapse collapse"
        aria-labelledby="heading"
      >
        <div class="accordion-body">
          {{ project.description }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["project"],
  components: {},
  name: "ProjectInfo",
  data: function () {
    return {};
  },
  methods: {},
};
</script>


<style scoped>
.accordion {
  margin-top: 30px;
}
button {
  font-family: Montserrat;
  color: var(--blue1);
}
</style>
