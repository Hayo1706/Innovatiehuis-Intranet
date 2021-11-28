<template>
    <div class='filesview'>
       <p>Files View</p>
        <div class="container-fluid">
        <div class="row">
          <div v-for="file in files" :key="file.name" class="col-sm-2" >
            {{file.name}}</div>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  name: "FilesView",
  props: [

  ],
  data: function () {
    return { files: [
      {name:"New File", path:"./New_folder", type:"Word"},
      {name:"New File 1", path:"./New_folder", type:"PDF"},
      {name:"New File 2", path:"./New_folder", type:"Powerpoint"},
      {name:"New File 3", path:"./New_folder", type:"Excel"},
      {name:"New File 4", path:"./New_folder", type:"Word"},
      {name:"New File 5", path:"./New_folder", type:"PDF"},
      {name:"New File 6", path:"./New_folder", type:"Powerpoint"},
      {name:"New File 7", path:"./New_folder", type:"Excel"},
      ]};
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
  width: 68vw;
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