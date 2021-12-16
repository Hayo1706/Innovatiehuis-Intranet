<template>
    <div class='filesview'>
      <p>Files View</p>
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

      
       <form
        action="http://127.0.0.1:5000/api/projects/upload"
        method="POST"
        enctype="multipart/form-data"
      >
      <input type="file" name="files" multiple="true" />
      <input type="hidden" name="projectid" :value= this.projectid />
      <input type="hidden" name="path" value="" />
      <input type="submit"/>
    </form>
   
    </div>
</template>

<script>
import ProjectService from "@/services/ProjectService.js";
export default {
  name: "FilesView",
  props: [

  ],
  data: function () {
    return { 
      files: [],
      projectid: this.$route.params.id};
  },
  async created() {
    //this.$emit("newHeaderTitle", "NAAM + PAD");
    ProjectService.getFilesOfProject(this.$route.params.id)
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