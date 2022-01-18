<template>
  <div class="project-listing">
    <div class="row">
      <VerticalHeader class="d-block d-lg-none"></VerticalHeader>
      <!-- small screens-->
      <div class="col-3 d-block d-lg-none">
        <div class="name-button mobileRow" @click="onClick()">
          {{ projectname }}
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
        <div class="mobileRow">
          <div id="archivedText" v-if="project.is_archived">Gearchiveerd</div>
          <div v-else>Niet gearchiveerd</div>
        </div>
      </div>

      <!-- large screens-->
      <div
        title="Open projectpagina"
        class="col-3 d-none d-lg-flex align-items-center justify-content-center"
        @click="onClick()"
      >
        <div class="name-button">
          {{ projectname }}
        </div>
      </div>
      <div
        title="Aangemaakt"
        class="col d-none d-lg-flex align-items-center justify-content-center"
      >
        {{
          project.created.toLocaleString("nl-NL", {
            day: "numeric",
            month: "numeric",
            year: "numeric",
          })
        }}
      </div>
      <div
        title="Laatst aangepast"
        class="col d-none d-lg-flex align-items-center justify-content-center"
      >
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
      <div
        class="col d-none d-lg-flex align-items-center justify-content-center"
      >
        <div id="archivedText" v-if="project.is_archived">Gearchiveerd</div>
        <div v-else>Niet gearchiveerd</div>
      </div>

      <div class="col-lg d-lg-flex align-items-center justify-content-center">
        <span class="button-span-right">
          <ProjectButtons
            @removeProject="(id) => $emit('removeProject', id)"
            @archiveProject="(_project) => $emit('archiveProject', _project)"
            v-bind:project="project"
          ></ProjectButtons>
        </span>
      </div>
    </div>
    <ProjectInfo
      @nameOrDescriptionChanged="
        (project_obb) => {
          this.projectname = project_obb.project_name;
        }
      "
      v-bind:project="project"
    ></ProjectInfo>
  </div>
</template>

<script>
import VerticalHeader from "./VerticalHeader.vue";
import ProjectButtons from "./ProjectButtons.vue";
import ProjectInfo from "@/shared_components/ProjectInfo.vue";
export default {
  props: ["project"],
  components: { VerticalHeader, ProjectButtons, ProjectInfo },
  name: "ProjectListing",
  data: function () {
    return {
      projectname: "",
    };
  },
  mounted() {
    this.projectname = this.project.project_name;
  },
  methods: {
    onClick() {
      this.$router.push("/project/" + this.project.projectid);
    },
  },
};
</script>

<style scoped>
.project-listing {
  box-sizing: border-box;
  color: var(--blue1);
  overflow: visible;
  background: linear-gradient(
    to right top,
    rgba(230, 230, 230, 0.7),
    rgba(230, 230, 230, 0.9)
  );
  border-radius: 0.5rem;
  margin-bottom: 0.3rem;
  font-size: 1.6vh;
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
.name-button{
  border-radius: 0.5rem 0px 0px 0px;
  background-color: var(--blue2);
  width: 100%;
  height: 100%;
  align-items: center;
  display: flex;
  cursor: pointer;
  font-size: 14pt;
  color: white;
  padding: 6px;
  text-decoration: none;
}
.name-button:hover{
  background-color: var(--blue1);
  color: white;
}
.mobileRow {
  height: 50px;
}
#archivedText {
  color: purple;
}
.button-span-right{
  margin-left: auto;
}
.iconHolder {
  padding: 5px;
}
</style>