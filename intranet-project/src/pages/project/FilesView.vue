<template>
    <div class='filesview'>
       <p>Files View</p>
        <table>
          <tr>
          <span v-for="file in files" :key="file.name">
          <td>{{file.name}}</td>
          </span>
          </tr>
      </table>
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
    background-color: #28418a;
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
img {
  height: width;
  padding-right: 1vw;
  padding-bottom: 0.5vh;
}
table{
  width: 100%;
  color: black;
  font-size: calc(0.75vw + 0.75vh);;
}
td{
  width: calc(68vw / 8);
  height: calc(68vw / 8);
}
</style>