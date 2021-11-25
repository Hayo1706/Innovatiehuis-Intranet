<template>
    <div>
      <p>Folders View</p>
      <table>
        <tr v-for="folder in folders" :key="folder.name">
          <td v-if="folder.shared == 'no'"><img src=".\..\..\assets\images\folder.png"/> {{folder.name}}</td>
          <td v-if="folder.shared == 'yes'"><img src=".\..\..\assets\images\shared_folder.png"/> {{folder.name}}</td>
        </tr>
      </table>
    </div>
</template>

<script>
export default {
  name: "FoldersView",
  props: [

  ],
  data: function () {
    return { folders: [
      {name:"New Folder", path:"./New_folder", shared:"no"},
      {name:"New Folder", path:"./New_folder", shared:"no"},
      {name:"New Folder", path:"./New_folder", shared:"no"},
      {name:"Gedeelde Folder", path:"./New_folder", shared:"yes"},
      ]};
  },
  methods: {
    onClick() {
      this.$router.push("/project/" + this.projectId + "/path");
    },
  },
}
</script>


<style scoped>
p {
  color: white;
  font-size: calc(1vw + 1vh);
  height: 100%;
  width: 68vw;
  margin: 0;
  text-align: center;
  background-color: #747579;
  border-style: outset;
  }
.project-folder {
  font-size: 16pt;
  font-weight: bold;
  background-color: #c6992f;
  color: #28418a;
  width: 300px;
  height: 60px;
  border-style: outset;
  text-align: center;
  justify-content: center;
  align-items: center;
  display: flex;
  border-radius: 8px;
}
img {
  height: 5vh;
  padding-right: 20px;
  cursor: pointer;
}
tr {
  display: inline-block;
}
td {
  width: 17vw;
}
table {
  width: 68vw;
}
</style>