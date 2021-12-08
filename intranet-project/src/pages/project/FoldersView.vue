<template>
    <div>
      <ProjectFolderHeader
      @newFolderAdded="(id) => addFolder(id)"/>
      <div class="container-fluid">
        <div class="row">
          <div v-for="folder in folders" :key="folder.name" class="col-sm-3">
            <ProjectFolder
              :naam="folder.name"
              :path="folder.path"
              :shared="folder.shared"
            />
            </div>
        </div>
      </div>
    </div>
</template>

<script>
import ProjectFolderHeader from "./ProjectFolderHeader.vue";
import ProjectFolder from "./ProjectFolder.vue";
export default {
  components: {
    ProjectFolderHeader,
    ProjectFolder,
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
    addFolder(val){
      if(this.path != null){
              alert(this.newFolderName);
         this.folders.push({name: val, path: this.path + "/" + val, shared: "no"});
      }
      this.folders.push({name: val, path: val, shared: "no"});
    },
  },
}
</script>


<style scoped>
.row{
  font-size: calc(0.7vw + 0.7vh);
  text-align: left;
}
</style>