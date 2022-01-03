<template>
  <div id="project-listing">
    <div class="row">
      <VerticalHeader class="d-block d-lg-none"></VerticalHeader>
      <!-- small screens-->
      <div class="col d-block d-lg-none">
        <div class="projectButton mobileRow" @click="onClick()">
          {{ project.project_name }}
        </div>
        <div class="mobileRow">
          {{
            project.created.toLocaleString("nl-NL", {
              day: "numeric",
              month: "numeric",
              year: "numeric",
            })
          }}
        </div>
        <div class="mobileRow">
          {{
            project.last_updated.toLocaleString("nl-NL", {
              day: "numeric",
              month: "numeric",
              year: "numeric",
              hour: "numeric",
              minute: "numeric",
              second: "numeric",
            })
          }}
        </div>
      </div>

      <!-- large screens-->
      <div class="col d-none d-lg-block" @click="onClick()">
        <div class="full-button">
          {{ project.project_name }}
        </div>
      </div>
      <div class="col d-none d-lg-block">
        {{
          project.created.toLocaleString("nl-NL", {
            day: "numeric",
            month: "numeric",
            year: "numeric",
          })
        }}
      </div>
      <div class="col d-none d-lg-block">
        {{
          project.last_updated.toLocaleString("nl-NL", {
            day: "numeric",
            month: "numeric",
            year: "numeric",
            hour: "numeric",
            minute: "numeric",
            second: "numeric",
          })
        }}
      </div>

      <div class="col">
        <ProjectButtons
          @removeProject="(id) => $emit('removeProject', id)"
          @archiveProject="(_project) => $emit('archiveProject', _project)"
          v-bind:project="project"
        ></ProjectButtons>
      </div>
    </div>
  </div>
</template>

<script>
import VerticalHeader from "./VerticalHeader.vue";
import ProjectButtons from "./ProjectButtons.vue";
export default {
  props: ["project"],
  components: { VerticalHeader, ProjectButtons },
  name: "ProjectListing",
  data: function () {
    return {};
  },
  methods: {
    onClick() {
      this.$router.push("/project/" + this.project.projectid);
    },
    loadParentsModal() {},
    loadChildrenModal() {},
  },
};
</script>

<style scoped>
#project-listing {
  padding: 10px;
  box-sizing: border-box;
  color: var(--blue1);
  overflow: visible;
  background: linear-gradient(
    to right top,
    rgba(230, 230, 230, 0.7),
    rgba(230, 230, 230, 0.9)
  );
  border-radius: 1rem;
  margin-bottom: 1vh;
  font-size: 2vh;
  border: solid var(--gold1) 2px;
}
.row {
  padding-top: 12px;
}
.projectButton {
  font-weight: bold;
  background-color: var(--gold2);
  color: var(--blue1);
  border-style: outset;
  border-radius: 8px;
  padding-left: 10px;
  padding-right: 10px;
  height: fit-content;
  cursor: pointer;
  width: fit-content;
}
.mobileRow {
  height: 53px;
}
</style>