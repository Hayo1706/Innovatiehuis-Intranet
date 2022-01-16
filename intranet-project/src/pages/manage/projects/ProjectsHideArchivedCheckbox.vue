<template>
  <div style="float: right;">
    <label class="switch" style="float: right;">
    
      <input
        id="hidearchivedcheckbox"
        type="checkbox"
        name="hidearchivedcheckbox"
        v-model="hideArchivedField"
        checked
      />
      <span class="slider round"></span>
    </label>
    <i style="float: right; font-size: 14pt; color: rgba(255,255,255,0.7)">Verberg gearchiveerde projecten</i>
  </div>
</template>
<script>
export default {
  name: "ProjectsHideArchivedCheckbox",
  props: ["hideArchived"],
  data: function () {
    return { hideArchivedField: true };
  },
  methods: {},
  watch: {
    hideArchivedField: function (val) {
      //do something when the data changes.
      if (!val) {
        this.$emit("hideArchived", false);
      } else {
        this.$emit("hideArchived", true);
      }
    },
    hideArchived: function (val) {
      this.hideArchivedField = val;
    },
  },
};
</script>
<style  scoped>
.switch {
  position: relative;
  display: inline-block;
  margin-left: 1em;
  width: 60px;
  height: 34px;
}

.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: var(--blue2);
}

input:focus + .slider {
  box-shadow: 0 0 1px var(--blue2);
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>