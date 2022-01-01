<template>
    <div>
      <ProjectFilesHeader 
        @searchBarChanged="setSearchTerm"
        @newFilesUploaded="reloadPage()"
      />
         
      <div class="container-fluid"> 
        <div class="row">
          <div v-for="file in files" :key="file" class="col-sm-2" > <!--- Determine size of each Column --->
            <div v-if="fileNameInSearchterm(file)"> <!--- Ensures that height is equal to width --->
              <ProjectFile
                :projectid="this.$route.params.id"
                :name="file"
                :type="file.split('.').pop()"
                :path="this.path.split(this.projectid)[1] + '/' + file"
                :shared='no'
                @fileDeleted="reloadPage()"
              />
            </div>
          </div>
        </div>
      </div>   
    </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import ProjectFilesHeader from "./ProjectFilesHeader.vue";
import ProjectFile from "./ProjectFile.vue";
export default {
  components: {
    ProjectFilesHeader,
    ProjectFile
  },
  name: "FilesView",
  props: {
    path: { type: String, required: true },
  },
  data: function () {
    return { 
      files: [],
      projectid: this.$route.params.id,
      searchTerm: "",
      currentPath: this.path,
      };
  },
  methods: {
    fileNameInSearchterm(name){
      if(name.includes(this.searchTerm) || this.searchTerm == null){
        return true;
      }
      else{
        return false;
      }
    },
     setSearchTerm(value) {
      this.searchTerm = value;
    },
    setPath(path){
      this.currentPath = path;
    },
    setFiles(){
      FilestorageService.getFilesOfPath(this.projectid, this.path.split(this.projectid)[1])
      .then((response) => {
        this.files = response;
      })
      .catch((err) => {
        if (err.response) {
          console.log(err.response.status);
        }
        alert(err);
      });
    },
    reloadPage(){
      location.reload();
    }
  },
  async created() {
    this.setFiles();
    //this.$parent.$on('pathChanged', this.setPath);
    //this.$emit("newHeaderTitle", "NAAM + PAD");
    
  },
}
</script>

<style scoped>
p {
    background-color: var(--blue1);
}
.filesview {
  color: white;
  font-size: calc(1vw + 1vh);
  font-family: AddeleSemiBold;
  height: 100%;
  margin: calc(1vw + 1vh);
  text-align: center;
}
.container-fluid{
  color: black;
}
.row{
  font-size: calc(0.7vw + 0.7vh);
  text-align: left;
}

</style>