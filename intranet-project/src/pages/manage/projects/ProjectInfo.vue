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
          @click="this.onParentsClick()"
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
          <div
            class="full-button"
            v-for="parent in this.parents"
            v-bind:key="parent.projectid"
            @click="navigate(parent.projectid)"
          >
            {{ parent.project_name }}
          </div>
          <div v-if="this.parents.length == 0">Geen resultaten</div>
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
          @click="this.onChildrenClick()"
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
          <div
            class="full-button"
            v-for="child in this.children"
            v-bind:key="child.projectid"
            @click="navigate(child.projectid)"
          >
            {{ child.project_name }}
          </div>
          <div v-if="this.children.length == 0">Geen resultaten</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ProjectService from "@/services/ProjectService.js";
export default {
  props: ["project"],
  components: {},
  name: "ProjectInfo",
  data: function () {
    return {
      parents: [],
      children: [],
      parentsOpen: false,
      childrenOpen: false,
    };
  },
  methods: {
    onParentsClick() {
      if (!this.parentsOpen) {
        ProjectService.getParentsById(this.project.projectid)
          .then((response) => {
            //remove the project from the view
            this.parents = response;
          })
          .catch((err) => {
            //invalid operation on server
            if (err.response) {
              console.log(err.response.status);
            }
          });
      }
      this.parentsOpen = !this.parentsOpen;
    },
    onChildrenClick() {
      if (!this.childrenOpen) {
        ProjectService.getChildrenById(this.project.projectid)
          .then((response) => {
            //remove the project from the view
            this.children = response;
          })
          .catch((err) => {
            //invalid operation on server
            if (err.response) {
              console.log(err.response.status);
            }
          });
      }
      this.childrenOpen = !this.childrenOpen;
    },
    navigate(projectid) {
      this.$router.push("/project/" + projectid);
    },
  },
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
.full-button {
  width: fit-content;
}
</style>
