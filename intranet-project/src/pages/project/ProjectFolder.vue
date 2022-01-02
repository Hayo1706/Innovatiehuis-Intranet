<template>
  <div class="projectFolder" @click.right="viewMenu = true" @mouseleave="viewMenu = false">
    <div class="container-fluid" @mouseleave="renameFolder()">
      <div class="row">
        <div class="col-sm-3">
          <img class="foldersImage" @click="goToFolder()" v-if="this.shared != 'yes'" src=".\..\..\assets\images\folder.png"/> 
          <img class="foldersImage" @click="goToFolder()" v-if="this.shared == 'yes'" src=".\..\..\assets\images\shared_folder.png"/> 
        </div>
        <div class="col-sm-9" @dblclick="editName = true">
          <input class="folderName" v-if="this.editName == true" v-model="newName"/>
          <input class="folderName" disabled v-if="this.editName == false" v-model="folderName"/>
        </div>
      </div>
    </div>
    <div class="container" v-if="viewMenu == true">
      <div class="row"><button @click="deleteFolder()">Verwijder</button></div>
      <div class="row">
        <button  
          data-bs-toggle="modal"
          data-bs-target="#moveModal">
          Verplaats
          </button>
        </div>
    </div>
    
    <div
      class="modal fade"
      id="moveModal"
      tabindex="-1"
      aria-labelledby="moveModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="moveModalLabel">
              Verplaatsen naar
            </h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-9" v-if="this.folders.length == 1">
                <h9>There are no folders to move to</h9>
              </div>
              <div class="mb-9" v-for="folder in this.folders" :key="folder">
                <button v-if="folder != this.name" @click="moveToFolder(folder)">{{folder}}</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
export default {
  name: "ProjectFolder",
  props: {
    projectid: { type: String, required: true},
    name: { type: String, required: true },
    path: { type: String, required: true },
    shared: { type: String, required: true },
    directorypath: { type: String, required: true },
  },
  data: function () {
    return {
      viewMenu: false,
      folderName: this.name,
      newName: this.name,
      editName: false,
      folders: []
    };
  },
  methods: {
    deleteFolder(){
      FilestorageService.deleteFolder(this.projectid, this.path)
      .then(() => {
        location.reload();
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });
    },
    renameFolder(){
      this.editName = false;
      if(!(this.newName == this.folderName)){
        FilestorageService.renameFolder(this.projectid, this.path, "", this.newName)
        .then(() => {
          this.editName = false;
          this.folderName = this.newName;
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
          alert(err);
        });
      }
    }, 
    moveToFolder(folder){
      var folder_path = this.directorypath + "/" + folder
      FilestorageService.moveFolder(this.projectid, this.path, folder_path, "")
      .then(() => {
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });
    },
    getFolders(path){
      FilestorageService.getFoldersOfProject(this.projectid, path)
      .then((response) => {
        this.folders = response;
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });
    },
    goToFolder(){
      this.$emit("currentPathChanged", this.path);
    } 
  },
  async created() {
    //this.$emit("newHeaderTitle", "NAAM + PAD");
    this.getFolders(this.directorypath);
  }
};
</script>

<style scoped>
.projectFolder{
  color: white;
  width: 100%;
  min-height: calc(1.5vw + 1.5vh);
  font-size: calc(0.5vh + 0.5vw)
}
.foldersImage{
  width: calc(1.5vw + 1.5vh);
}
.folderName{
  background-color: transparent;
  color: white;
  border: 0px;
}
.container{
  margin-top: 2vh;
}
h5, h9{
  color: black;
}

</style>