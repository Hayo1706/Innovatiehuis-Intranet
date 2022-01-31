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
            v-show="this.uploadMenu == true"
            @change="uploadFiles"
            type="file"
            id="files"
            name="files"
            multiple
            hidden
          />
          <label v-show="this.uploadMenu == true" for="files" refs="files" class="file-btn">
            <img
              title="Upload bestand"
              class="component-header-button"
              src=".\..\..\assets\images\new_upload.png"
            />
          </label>
          <div
            title="Uploading bestanden..."
            v-show="this.uploadMenu == false"
            class="spinner-border"
            role="status"
            alt="uploading..."
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FilestorageService from "@/services/FilestorageService.js";
import PermissionService from "@/services/PermissionService.js";
import SearchBar from "@/shared_components/SearchBar.vue";
import AlertService from "../../services/AlertService";

export default {
  name: "ProjectFilesHeader",
  components: {
    SearchBar,
  },
  props: ["path"],
  data: function () {
    return {
      files: [],
      uploadMenu: true,
    };
  },
  methods: {
    async uploadFiles(e) {
      const ok = await this.$refs.confirmDialogue.show({
        title: "Waarschuwing",
        message:
          'Het Innovatieplatform is een platform deels toegankelijk voor studenten en derden die beperkte screening hebben doorstaan. Weet je zeker dat deze bestanden gedeeld mogen worden via dit platform?',
      });
      if (ok) {
        this.uploadMenu = false;
        var files = e.target.files;
        var amountOfFiles = files.length;
        for (let i = 0; i < files.length; i++) {
          var formData = new FormData();
          formData.append(files[i].name, files[i]);

          FilestorageService.uploadFiles(
            this.$route.params.id,
            this.path,
            formData
          )
            .then((response) => {
              amountOfFiles--;
              if (amountOfFiles == 0) {
                this.uploadMenu = true;
              }
              AlertService.handleSuccess(response);
              this.$emit("newFilesUploaded");
            })
            .catch((err) => {
              amountOfFiles--;
              if (amountOfFiles == 0) {
                this.uploadMenu = true;
              }
              AlertService.handleError(err);
              if (err.response.status === 409) {
                var confirmation = confirm(err.response.data.response.message);
                FilestorageService.uploadFile(
                  this.$route.params.id,
                  this.path,
                  formData,
                  confirmation
                )
                  .then((response) => {
                    amountOfFiles--;
                    if (amountOfFiles == 0) {
                      alert()
                      this.uploadMenu = true;
                    }
                    AlertService.handleSuccess(response);
                    this.$emit("newFilesUploaded");
                  })
                  .catch((err) => {
                    amountOfFiles--;
                    if (amountOfFiles == 0) {
                      this.uploadMenu = true;
                    }
                    AlertService.handleError(err);
                  });
              }
            });
        }
        document.getElementById("files").value = null;
      }
    },
    canUploadFile() {
      return PermissionService.userHasPermission(
        "may_update_file_in_own_project"
      );
    },
  },
};
</script>
