<template>
    <div class='folderview'>
      <p>Folders View</p>
      <div class="container-fluid">
        <div class="row">
          <div v-for="folder in folders" :key="folder.name" class="col-sm-3">
            <img v-if="folder.shared == 'no'" src=".\..\..\assets\images\folder.png"/> 
            <img v-if="folder.shared == 'yes'" src=".\..\..\assets\images\shared_folder.png"/> 
            {{folder.name}}</div>
        </div>
      </div>
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
      this.$router.push("/projects/" + this.projectId + "/path");
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
.container-fluid{
  color: black;
}
.row{
  font-size: calc(0.7vw + 0.7vh);
  text-align: left;
}
</style>