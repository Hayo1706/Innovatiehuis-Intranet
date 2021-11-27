<template>
    <div class='folderview'>
      <p>Folders View</p>
        <table>
          <tr>
          <span v-for="folder in folders" :key="folder.name">
          <td v-if="folder.shared == 'no'"><img src=".\..\..\assets\images\folder.png"/> {{folder.name}}</td>
          <td v-if="folder.shared == 'yes'"><img src=".\..\..\assets\images\shared_folder.png"/> {{folder.name}}</td>
          </span>
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
    background-color: var(--blue1);
}
.folderview {
  color: white;
  font-size: calc(1vw + 1vh);
  font-family: AddeleSemiBold;
  height: 100%;
  width: 68vw;
  margin: calc(1vw + 1vh);
  text-align: center;
}
img {
  height: 7vh;
  padding-right: 1vw;
  padding-bottom: 0.5vh;
}
table{
  width: 100%;
  color: black;
}
td{
  width: calc(68vw / 4);
}
</style>