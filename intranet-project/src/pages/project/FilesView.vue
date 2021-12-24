<template>
    <div>
      <ProjectFilesHeader>
      </ProjectFilesHeader>  
      <div class="container-fluid"> 
        <div class="row">
          <div v-for="file in files" :key="file" class="col-sm-2" > <!--- Determine size of each Column --->
            <div class="box"> <!--- Ensures that height is equal to width --->
              <div class = "content"> <!--- Position of content is absolute --->
                {{file}}
              </div>
            </div>
          </div>
        </div>
      </div>   
    </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import ProjectFilesHeader from "./ProjectFilesHeader.vue";
export default {
  components: {
    ProjectFilesHeader
  },
  name: "FilesView",
  props: [

  ],
  data: function () {
    return { 
      files: [],
      projectid: this.$route.params.id};
  },
  methods: {
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
    top:      0;
    left:     0;
    bottom:   0;
    right:    0;
    font-size: 12px;
}

</style>