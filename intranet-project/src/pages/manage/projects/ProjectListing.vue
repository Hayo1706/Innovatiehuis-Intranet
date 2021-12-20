<template>
  <div class="project-listing">
    <div class="row">
      <VerticalHeader class="d-block d-lg-none"></VerticalHeader>
      <!-- small screens-->
      <div class="col d-block d-lg-none">
        <div class="projectButton mobileRow" @click="onClick()">
          {{ project.name }}
        </div>
        <div class="mobileRow">
          {{
            project.createdat.toLocaleString("nl-NL", {
              day: "numeric",
              month: "numeric",
              year: "numeric",
            })
          }}
        </div>
        <div class="mobileRow">
          {{
            project.lastupdated.toLocaleString("nl-NL", {
              day: "numeric",
              month: "numeric",
              year: "numeric",
              hour: "numeric",
              minute: "numeric",
              second: "numeric",
            })
          }}
        </div>
        <div class="mobileRow">
          <br /><span
            @click="onParrentClick()"
            class="projectButton"
            v-if="project.parentname"
            >{{ project.parentname }}</span
          >
        </div>
        <div class="mobileRow">{{ project.amountsubprojects }}</div>
      </div>

      <!-- large screens-->
      <div class="col d-none d-lg-block" @click="onClick()">
        <div class="projectButton">
          {{ project.name }}
        </div>
      </div>
      <div class="col d-none d-lg-block">
        {{
          project.createdat.toLocaleString("nl-NL", {
            day: "numeric",
            month: "numeric",
            year: "numeric",
          })
        }}
      </div>
      <div class="col d-none d-lg-block">
        {{
          project.lastupdated.toLocaleString("nl-NL", {
            day: "numeric",
            month: "numeric",
            year: "numeric",
            hour: "numeric",
            minute: "numeric",
            second: "numeric",
          })
        }}
      </div>
      <div class="col d-none d-lg-block">
        <span
          @click="onParrentClick()"
          class="projectButton"
          v-if="project.parentname"
          >{{ project.parentname }}</span
        >
      </div>
      <div class="col d-none d-lg-block">{{ project.amountsubprojects }}</div>

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
    onParrentClick() {
      this.$router.push("/project/" + this.project.parentid);
    },
  },
};
</script>

<style scoped>
.project-listing {
  background-color: var(--blue3);
  margin: 3px;
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
  margin-bottom: 10px;
  box-sizing: border-box;
  cursor: pointer;
  width: fit-content;
}
.mobileRow {
  height: 50px;
}
</style>