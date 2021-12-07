<template>
    <div>
      <ProjectFolderHeader
      @newFolderAdded="addFolder"/>
      <div class="container-fluid">
        <div class="row">
          <div v-for="folder in folders" :key="folder.name" class="col-sm-3" @click="goToDirectory(folder.path)">
            <img class="foldersImage" v-if="folder.shared == 'no'" src=".\..\..\assets\images\folder.png"/> 
            <img class="foldersImage" v-if="folder.shared == 'yes'" src=".\..\..\assets\images\shared_folder.png"/> 
            {{folder.name}}</div>
        </div>
      </div>
    </div>
</template>

<script>
import ProjectFolderHeader from "./ProjectFolderHeader.vue";
export default {
  components: {
    ProjectFolderHeader,
  },
  name: "FoldersView",
  props: [

  ],
  data: function () {
    return { folders: [
      {name:"Requirements", path:"./Requirements", shared:"no"},
      {name:"Architectuur", path:"./Architectuur", shared:"no"},
      {name:"Classified", path:"./Classified", shared:"no"},
      {name:"Gedeelde Folder", path:"./Gedeelde Folder", shared:"yes"},
      ],
      path: null};
  },
  methods: {
    goToDirectory(path) {
       this.$router.push(this.$route.params.id + "/" + path);
    },
    addFolder(val){
      
      if(this.path != null){
         this.folders.append({name: val, path: this.$route.params.id + "/" + this.path + "/" + val, shared: "no"});
      }
      this.folders.append({name: val, path: this.$route.params.id + "/" + val, shared: "no"});
    }
  },
}
</script>


<style scoped>
.foldersImage {
  height: calc(2vw + 5vh);
  padding-right: 1vw;
  padding-bottom: 0.5vh;
}
.row{
  font-size: calc(0.7vw + 0.7vh);
  text-align: left;
}
</style>