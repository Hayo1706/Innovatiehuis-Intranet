<template>
    <div>
      <ProjectFilesHeader 
        @searchBarChanged="setSearchTerm"
        @newFilesUploaded="reloadFiles()"
      />
         
      <div class="container-fluid"> 
        <div class="row">
          <div v-for="file in files" :key="file" class="col-sm-2" > <!--- Determine size of each Column --->
            <div v-if="fileNameInSearchterm(file)"> <!--- Ensures that height is equal to width --->
              <ProjectFile
                :projectid="this.$route.params.id"
                :name="file"
                :type="file.split('.').pop()"
                :path="'/' + file"
                :shared='no'
                @fileDeleted="reloadFiles()"
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
  props: [

  ],
  data: function () {
    return { 
      files: [],
      projectid: this.$route.params.id,
      searchTerm: "",
      path: this.$route.fullPath.split("/project/" + this.$route.params.id)[1]
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
    reloadFiles(){
      location.reload();
    },
  },
  async created() {
    //this.$emit("newHeaderTitle", "NAAM + PAD");
    FilestorageService.getFilesOfProject(this.$route.params.id)
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
}
</script>

<style scoped>
p {
    background-color: var(--blue1);
}
.filesview {
  color: white;
  font-size: calc(1vw + 1vh);
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