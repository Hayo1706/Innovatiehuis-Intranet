<template>
  <div class="projectFolder" @click.right="viewMenu = true" @mouseleave="viewMenu = false">
    <div class="container-fluid" @mouseleave="renameFolder()">
      <div class="row">
        <div class="col-sm-3">
          <img class="foldersImage" v-if="this.shared != 'yes'" src=".\..\..\assets\images\folder.png"/> 
          <img class="foldersImage" v-if="this.shared == 'yes'" src=".\..\..\assets\images\shared_folder.png"/> 
        </div>
        <div class="col-sm-9" @dblclick="editName = true">
          <input class="folderName" v-if="this.editName == true" v-model="folderName"/>
          <input class="folderName" disabled v-if="this.editName == false" v-model="folderName"/>
        </div>
      </div>
    </div>
    <div class="container" v-if="viewMenu == true">
      <div class="row"><button @click="deleteFolder()">Remove</button></div>
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
  },
  data: function () {
    return {
      viewMenu: false,
      folderName: this.name,
      editName: false
    };
  },
  methods: {
    deleteFolder(){
      FilestorageService.deleteFolder(this.projectid, this.path)
      .then((response) => {
        location.reload();
        alert(response);
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });
    },
    renameFolder(){
      FilestorageService.renameFolder(this.projectid, this.path, "", this.folderName)
      .then(() => {
         this.editName = false;
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });
    },  
  },
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
</style>