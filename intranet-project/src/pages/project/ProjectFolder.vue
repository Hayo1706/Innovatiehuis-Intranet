<template>
  <div
    class="projectFolder"
    @click.right="viewMenu = true"
    @mouseleave="viewMenu = false; moveMenu = false"
  >
    <div class="container-fluid" @mouseleave="renameFolder()">
      <div class="row">
        <div class="col-sm-3">
          <img
            class="foldersImage"
            @click="goToFolder()"
            v-if="this.shared != 'yes'"
            src=".\..\..\assets\images\folder.png"
          />
          <img
            class="foldersImage"
            @click="goToFolder()"
            v-if="this.shared == 'yes'"
            src=".\..\..\assets\images\shared_folder.png"
          />
        </div>
        <div class="col-sm-9" @dblclick="editName = true">
          <input
            class="folderName"
            v-if="this.editName == true"
            v-model="newName"
          />
          <input
            class="folderName"
            disabled
            v-if="this.editName == false"
            v-model="folderName"
          />
        </div>
      </div>
    </div>
    <div class="container" v-if="viewMenu == true">
      <div class="row"><button @click="deleteFolder()">Verwijder</button></div>
      <div class="row">
        <button @click="moveMenu = true; getFolders()">Verplaats</button>
      </div>
    </div>
    <div class="container" v-if="moveMenu == true">
      <div v-if="this.folders.length > 1">
        <div class="row" v-for="folder in this.folders" :key="folder">
          <button v-if="folder != this.name" @click="moveToFolder(folder)">
            {{ folder }}
          </button>
        </div>
      </div>
      <div v-else>
        <h9>There are no folders to move to</h9>
      </div>
    </div>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
export default {
  name: "ProjectFolder",
  props: {
    projectid: { type: String, required: true },
    name: { type: String, required: true },
    path: { type: String, required: true },
    shared: { type: String, required: true },
    directorypath: { type: String, required: true },
  },
  data: function () {
    return {
      viewMenu: false,
      moveMenu: false,
      folderName: this.name,
      newName: this.name,
      editName: false,
      folders: [],
    };
  },
  methods: {
    deleteFolder() {
      FilestorageService.deleteFolder(this.projectid, this.path, false)
        .then(() => {
          this.$emit("folderDeleted");
        })
        .catch((err) => {
          if(err.response.status === 409){
            if(confirm("There are elements within this folder, are you sure?")){
              FilestorageService.deleteFolder(this.projectid, this.path, true)
              .then(() => {
                this.$emit("folderDeleted");
              })
              .catch((err) => {
                  if (err.response) {
                    console.log(err.response);
                }
              });
              console.log(err.response.status)
            }
            console.log(err.response.status)
          }

          if (err.response) {
            console.log(err.response);
          }
        });
    },
    renameFolder() {
      this.editName = false;
      if (!(this.newName == this.folderName)) {
        FilestorageService.renameFolder(
          this.projectid,
          this.path,
          "",
          this.newName
        )
          .then(() => {
            this.editName = false;
            this.folderName = this.newName;
          })
          .catch((err) => {
            if (err.response) {
              console.log(err.response.status);
            }
          });
      }
    },
    moveToFolder(folder) {
      var folder_path = this.directorypath + "/" + folder;
      FilestorageService.moveFolder(this.projectid, this.path, folder_path, "")
        .then((response) => {
          if (response.status == 400) {
            alert(response);
          }
          this.$emit("folderMoved");
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    getFolders() {
      FilestorageService.getFoldersOfProject(this.projectid, this.directorypath)
        .then((response) => {
          this.folders = response;
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    goToFolder() {
      this.$emit("currentPathChanged", this.path);
    },
  },
  async created() {
    //this.$emit("newHeaderTitle", "NAAM + PAD");
    this.getFolders();
  },
};
</script>

<style scoped>
.projectFolder {
  color: white;
  width: 100%;
  min-height: calc(1.5vw + 1.5vh);
  font-size: calc(0.5vh + 0.5vw);
}
.foldersImage {
  width: calc(1.5vw + 1.5vh);
}
.folderName {
  background-color: transparent;
  color: white;
  border: 0px;
}
.container {
  margin-top: 2vh;
}
h5,
h9 {
  color: black;
}
</style>