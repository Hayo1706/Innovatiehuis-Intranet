<template>
  <div>
    <div id="projectFilesHeader">
      <div class="row">
        <div class="col-sm-9">Files View</div>
        <div class="col-sm-2">
          <SearchBar
            @searchBarChanged="
              (searchTerm) => $emit('searchBarChanged', searchTerm)
            "
            v-bind:searchTerm="this.searchTerm"
          ></SearchBar>
        </div>
        <div class="col-sm-1">
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
            localStorage.clear();
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
    }    
  },
};
</script>

<style scoped>
#projectFilesHeader {
  color: white;
  font-size: calc(1vw + 1vh);
  font-family: AddeleSemiBold;
  margin: calc(1vw + 1vh);
  text-align: center;
  background-color: var(--blue1);
}
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