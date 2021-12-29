<template>
  <div class="projectFile" @click.right="viewMenu = true" @mouseleave="viewMenu = false">
    <div class = "box" @mouseleave="editName = false">
        <div class = "content" @dblclick="editName = true" @mouseleave="renameFile()"> <!--- Position of content is absolute --->
            <input v-if="editName == false" class="fileName" v-model="fileName" disabled/>
            <input v-if="editName == true" class="fileName" v-model="fileName"/>
            .{{this.fileType}}
        </div>
    </div>
    <div class="container" v-if="viewMenu == true">
        <div class="row"><button @click="downloadFile()">Download</button></div>
        <div class="row"><button @click="deleteFile()">Delete</button></div>
    </div>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
export default {
  name: "ProjectFile",
  props: {
    projectid: { type: String, required: true},
    name: { type: String, required: true },
    type: { type: String, required: false},
    path: { type: String, required: true },
    shared: { type: String, required: true },
  },
  data: function () {
    return {
      viewMenu: false,
      fileName: this.name.split(".")[0],
      editName: false,
      fileType: this.type,
    };
  },
  methods: {
      downloadFile(){
        FilestorageService.downloadFile(this.projectid, this.path)
        .then((response) => { 
          alert(response.data)
        })
      },
      deleteFile(){
        FilestorageService.deleteFile(this.projectid, this.path)
        .then((response) => {
            this.$emit('fileDeleted');
            alert(response)
        })
        .catch((err) => {
            if (err.response) {
            console.log(err.response.status);
            }
            alert(err);
        });
      },
      renameFile(){
        FilestorageService.updateFile(this.projectid, this.path)
        .then((response) => {
            this.editName = false;
            alert(response)
        })
        .catch((err) => {
            if (err.response) {
            console.log(err.response.status);
            }
            alert(err);
        });
    },  
  }
};
</script>

<style scoped>
.projectFile{
  color: white;
  width: 100%;
  min-height: calc(1.5vw + 1.5vh);
  font-size: calc(0.5vh + 0.5vw)
}
.fileName{
  background-color: transparent;
  color: white;
  border: 0px;
  width: 70%;
}
.box {
    position: relative;
    width:    100%; /* desired width */
    background-color: var(--blue2);
    margin-bottom: calc(1vw + 1vh);
}
.box:before {
    content:     "";
    display:     block;
    padding-top: 100%; /* initial ratio of 1:1*/
}

.content {
    position: absolute;
}
.container{
  margin-top: 2vh;
}
</style>