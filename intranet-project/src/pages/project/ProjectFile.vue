<template>
  <div class="projectFile" @click.right="viewMenu = true" @mouseleave="viewMenu = false">
    <div>
      <div class="row">
        <img v-if="this.type == 'pdf'" src=".\..\..\assets\images\pdficon.png"/>
        <img v-if="this.type == 'txt'" src=".\..\..\assets\images\txticon.png"/>
        <img v-if="this.type == 'docx'" src=".\..\..\assets\images\wordicon.jpg"/>
        <img v-if="this.type == 'pptx'" src=".\..\..\assets\images\powerpointicon.png"/>
        <img v-if="this.type == 'xlsx'" src=".\..\..\assets\images\excelicon.png"/>
      </div>
    </div>
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
      dictType: {
        pdf: "pdficon.png",
        docx: "wordicon.jpg",
        xlsx: "excelicon.png",
        pptx: "powerpointicon.png",
        txt: "txticon.png",
        unknown: "unknownfile.png",
      }
    };
  },
  methods: {
      downloadFile(){
        FilestorageService.downloadFile(this.projectid, this.path)
        .then((response) => { 
          const blob = new Blob([response.data], { type: response.headers["content-type"] })
          const link = document.createElement('a')
          link.href = URL.createObjectURL(blob)
          link.download = this.name
          link.click()
          URL.revokeObjectURL(link.href)
        }).catch(console.error)
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
        if(this.editName == true){
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
        }
      },
      getTypeImage(){
        if(this.fileType in this.dictType){
          alert("yes")
        }
      } 
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
.content {
    position: absolute;
}
.container{
  margin-top: 2vh;
}
</style>