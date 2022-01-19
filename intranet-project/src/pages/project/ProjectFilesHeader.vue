<template>
  <div>
    <div id="projectFilesHeader">
      <div class="row">
        <div class="col-8">
          <slot class="header"></slot>
        </div>
        <div class="col-3">
          <SearchBar
            @searchBarChanged="
              (searchTerm) => $emit('searchBarChanged', searchTerm)
            "
            placeholder="Filter op naam..."
            v-bind:searchTerm="this.searchTerm"
          ></SearchBar>
        </div>
        <div v-show="canUploadFile()" class="col-1">
          <input
            @change="uploadFiles"
            type="file"
            id="files"
            name="files"
            multiple
            hidden
          />
          <label for="files" refs="files" class="file-btn">
            <img
              title="Upload bestand"
              class="component-header-button"
              src=".\..\..\assets\images\new_upload.png"
            />
          </label>
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

        FilestorageService.uploadFiles(
          this.$route.params.id,
          this.path,
          formData
        )
          .then(() => {
            this.$emit("newFilesUploaded");
          })
          .catch((err) => {
            if (err.response.status === 409) {
              var confirmation = confirm(err.response.data.response.message);
              FilestorageService.uploadFiles(
                this.$route.params.id,
                this.path,
                formData,
                confirmation
              )
                .then(() => {
                  this.$emit("newFilesUploaded");
                })
                .catch((err) => {
                  if (err.response) {
                    console.log(err.response.status);
                  }
                });
            }
          });
      }
      document.getElementById("files").value = null;
    },
    canUploadFile() {
      return PermissionService.userHasPermission(
        "may_update_file_in_own_project"
      );
    },
  },
};
</script>
