<template>
  <div
    class="projectFile"
    @click.right="viewMenu = true"
    @mouseleave="viewMenu = false; moveMenu = false"
  >
    <div>
      <div class="row">
        <img
          v-if="this.type == 'pdf'"
          src=".\..\..\assets\images\pdficon.png"
        />
        <img
          v-if="this.type == 'txt'"
          src=".\..\..\assets\images\txticon.png"
        />
        <img
          v-if="this.type == 'docx'"
          src=".\..\..\assets\images\wordicon.jpg"
        />
        <img
          v-if="this.type == 'pptx'"
          src=".\..\..\assets\images\powerpointicon.png"
        />
        <img
          v-if="this.type == 'xlsx'"
          src=".\..\..\assets\images\excelicon.png"
        />
      </div>
    </div>
    <div class="box" @mouseleave="editName = false">
      <div
        class="content"
        @dblclick="editName = true"
        @mouseleave="renameFile()"
      >
        <!--- Position of content is absolute --->
        <input
          v-if="editName == false"
          class="fileName"
          v-model="fileName"
          disabled
        />
        <input v-if="editName == true" class="fileName" v-model="fileName" />
        .{{ this.fileType }}
      </div>
    </div>
    <div class="container" v-if="viewMenu == true">
      <div class="row"><button @click="downloadFile()">Download</button></div>
      <div class="row"><button @click="deleteFile()">Verwijder</button></div>
      <div class="row"><button @click="moveMenu = true; setFolders()">Verplaats</button></div>



      <div class="container" v-if="moveMenu == true">
        <div v-if="this.folders.length > 0">
          <div class="row" v-for="folder in this.folders" :key="folder">
            <button @click="moveFile(this.directorypath + '/' + folder)">
              {{ folder }}
            </button>
          </div>
        </div>
        <div v-else>
          <h9>There are no folders to move to</h9>
        </div>
      </div>



    </div>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
export default {
  name: "ProjectFile",
  props: {
    projectid: { type: String, required: true },
    name: { type: String, required: true },
    type: { type: String, required: false },
    path: { type: String, required: true },
    directorypath: { type: String, required: true },
    shared: { type: String, required: true },
  },
  data: function () {
    return {
      viewMenu: false,
      moveMenu: false,
      fileName: this.name.split(".")[0],
      editName: false,
      folders: [],
      fileType: this.type,
      dictType: {
        pdf: "pdficon.png",
        docx: "wordicon.jpg",
        xlsx: "excelicon.png",
        pptx: "powerpointicon.png",
        txt: "txticon.png",
        unknown: "unknownfile.png",
      },
    };
  },
  methods: {
      downloadFile(){
        FilestorageService.downloadFile(this.projectid, this.path)
        .then((response) => { 
          const url = window.URL.createObjectURL(new Blob([response.data]))
          const link = document.createElement('a')
          link.href = url;
          link.setAttribute('download', this.name);
          document.body.appendChild(link);
          link.click();
          link.href = window.URL.createObjectURL(new Blob());
        }).catch(console.error)
      },
      deleteFile(){
        FilestorageService.deleteFile(this.projectid, this.path)
        .then(() => {
          this.$emit("fileDeleted");
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    renameFile() {
      if (this.editName == true) {
        var newFileName = this.fileName + "." + this.fileType
        if(this.name != newFileName){
          FilestorageService.renameFile(this.projectid, this.path, newFileName)
            .then((response) => {
              this.editName = false;
              console.log(response.data);
              this.$emit("nameChanged");
            })
            .catch((err) => {
              if (err.response) {
                console.log(err.response.status);
              }
            });
        }
      }
    },
    setFolders() {
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
    moveFile(target_path) {
      FilestorageService.moveFile(this.projectid, this.path, target_path)
      .then(() => {
          this.$emit("fileMoved");
        })
        .catch((err) => {
          if (err.response) {
            console.log(err.response.status);
          }
        });
    },
    getTypeImage() {
      if (this.fileType in this.dictType) {
        alert("yes");
      }
    },
  },
};
</script>

<style scoped>
.projectFile {
  color: white;
  width: 100%;
  min-height: calc(1.5vw + 1.5vh);
  font-size: calc(0.5vh + 0.5vw);
}
.fileName {
  background-color: transparent;
  color: white;
  border: 0px;
  width: 70%;
}
.content {
  position: absolute;
}
.container {
  margin-top: 2vh;
}
</style>