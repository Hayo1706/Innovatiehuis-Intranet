<template>
  <div
    class="project-listing"
    v-bind:class="{ archived: this.project.is_archived }"
  >
    <div
      class="row collapsed accordion_button"
      type="button"
      data-bs-toggle="collapse"
      :data-bs-target="'#collapseName' + this.project.projectid"
      aria-expanded="false"
      :aria-controls="'collapseName' + this.project.projectid"
      :id="'collapseDetailsButton' + this.project.projectid"
      @click="this.open = !this.open"
    >
      <VerticalHeader class="d-block d-lg-none"></VerticalHeader>
      <!-- small screens-->
      <div class="col-3 d-block d-lg-none">
        <div class="mobileRow">
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
        class="
          name-wrapper
          col-3
          d-none d-lg-flex
          align-items-center
          justify-content-center
        "
      >
        {{ projectname }}
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
        <div id="archivedText" v-if="this.project.is_archived">
          Gearchiveerd
        </div>
        <div v-else>Niet gearchiveerd</div>
      </div>

      <div
        class="col col-lg d-lg-flex align-items-center justify-content-center"
      >
        <span class="button-span-right">
          <ProjectButtons
            @removeProject="(id) => $emit('removeProject', id)"
            @archiveProject="(_project) => $emit('archiveProject', _project)"
            v-bind:project="project"
          ></ProjectButtons>
        </span>
        <h2 class="accordion-header" :id="'heading' + this.project.projectid">
          <button
            class="full-button openProjectButton"
            type="button"
            @click.left="visitProjectPage()"
            @click.middle="visitProjectPage()"
          >
            <img src="@/assets/images/open_page.png" />
            Projectpagina
          </button>
        </h2>
      </div>
    </div>

    <div
      :id="'collapseName' + this.project.projectid"
      class="accordion-collapse collapse"
      aria-labelledby="heading"
    >
      <div class="accordion-body">
        <ProjectInfo
          v-bind:open="this.open"
          v-bind:project="project"
          @nameOrDescriptionChanged="
            (project_obb) => {
              this.projectname = project_obb.project_name;
            }
          "
        ></ProjectInfo>
      </div>
    </div>
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
      open: false,
    };
  },
  mounted() {
    this.projectname = this.project.project_name;
  },
  methods: {
    visitProjectPage() {
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
  background-color: rgb(234, 234, 234);
  /* margin-bottom: 0.3rem; */
  font-size: 1.6vh;
  border-bottom: 1px solid hsl(0deg 0% 86%);
}
.project-listing:last-child {
  border-bottom: none;
}
.project-listing:hover {
  background-color: rgb(230, 230, 230);
}
.archived {
  background-color: rgb(223, 223, 223);
}
.archived:hover {
  background-color: rgb(227, 227, 227);
}

.name-button {
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
.name-button:hover {
  background-color: var(--blue1);
  color: white;
}
.mobileRow {
  height: 50px;
}
#archivedText {
  color: purple;
}
.button-span-right {
  margin-left: auto;
}
.iconHolder {
  padding: 5px;
}
.name-wrapper {
  padding-right: 0;
}
.openProjectButton img {
  margin-right: 6px;
  height: 1em;
}
.openProjectButton {
  padding-right: 10px;
  padding-left: 10px;
}
.col {
  border-left: 1px solid hsl(0deg 0% 89%);
}
</style>