<template>
  <div>

    <div id="projectFilesHeader">
      <div class="row">
        <div class="col-sm-8"><slot></slot></div>
        <div class="col-sm-3">
          <SearchBar
            @searchBarChanged="
              (searchTerm) => $emit('searchBarChanged', searchTerm)
            "
            v-bind:searchTerm="this.searchTerm"
          ></SearchBar>
        </div>
        <div v-show="canUploadFile()" class="col-sm-1">
          <input
            @change="uploadFiles"
            type="file"
            id="files"
            name="files"
            multiple
            hidden
          />

          <button class="iconButton">
            <label for="files" refs="files" class="file-btn">
              <img
                class="iconImage"
                src=".\..\..\assets\images\new_upload.png"
              />
            </label>
          </button>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import PermissionService from "@/services/PermissionService.js";
import SearchBar from "@/shared_components/SearchBar.vue";
export default {
  name: "ProjectFilesHeader",
  components: {
    SearchBar,
  },
  props: ["path"],
  data: function () {
    return {
      files: [],
    };
  },
  methods: {
    uploadFiles(e) {
      var files = e.target.files;
      for (let i = 0; i < files.length; i++) {
        var formData = new FormData();
        formData.append(files[i].name, files[i]);

        FilestorageService.uploadFiles(this.$route.params.id, this.path, formData)
        .then(() => {
          this.$emit("newFilesUploaded")
        })
        .catch((err) => {
          if(err.response.status === 409){
            var confirmation = confirm(err.response.data.response.message)
            FilestorageService.uploadFiles(this.$route.params.id, this.path, formData, confirmation)
            .then(() => {
              this.$emit("newFilesUploaded")
            })
            .catch((err) => {
              if (err.response) {
                console.log(err.response.status);
              }
            });
          }
        });
      }
      document.getElementById("files").value=null;
    },
    canUploadFile(){
      return PermissionService.userHasPermission("may_update_file_in_own_project");
    },    
  },
};
</script>

<style scoped>
.iconButton {
  border: 0;
  background-color: transparent;
}
.iconImage {
  height: calc(1vw + 1vh);
  margin: 0 auto;
  display: block;
}
.input-group {
  margin: 0.5vh auto;
  height: 80%;
}
</style>