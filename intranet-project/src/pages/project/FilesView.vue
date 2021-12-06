<template>
    <div class='filesview'>
      <p>Files View</p>
      <div class="container-fluid"> 
        <div class="row">
          <div v-for="file in files" :key="file.name" class="col-sm-2" > <!--- Determine size of each Column --->
            <div class="drag-el" draggable> <!--- Make boxex draggable --->
              <div class="box"> <!--- Ensures that height is equal to width --->
                <div class = "content"> <!--- Position of content is absolute --->
                  {{file.name}}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  name: "FilesView",
  props: [

  ],
  data: function () {
    return { files: [
      {name:"New File", path:"./New_folder", type:"Word"},
      {name:"New File 1", path:"./New_folder", type:"PDF"},
      {name:"New File 2", path:"./New_folder", type:"Powerpoint"},
      {name:"New File 3", path:"./New_folder", type:"Excel"},
      {name:"New File 4", path:"./New_folder", type:"Word"},
      {name:"New File 5", path:"./New_folder", type:"PDF"},
      {name:"New File 6", path:"./New_folder", type:"Powerpoint"},
      {name:"New File 7", path:"./New_folder", type:"Excel"},
      ]};
  },
  startDrag (evt, item) {
        evt.dataTransfer.dropEffect = 'move'
        evt.dataTransfer.effectAllowed = 'move'
        evt.dataTransfer.setData('itemID', item.id)
  },
}
</script>


<style scoped>
p {
    background-color: var(--blue1);
}
.filesview {
  color: white;
  font-size: calc(1vw + 1vh);
  font-family: AddeleSemiBold;
  height: 100%;
  width: 68vw;
  margin: calc(1vw + 1vh);
  text-align: center;
}
.container-fluid{
  color: black;
}
.row{
  font-size: calc(0.7vw + 0.7vh);
  text-align: left;
}
.box {
    position: relative;
    width:    100%; /* desired width */
    background-color: var(--blue2);
    margin-bottom: calc(1vw + 1vh);
}
.box:before {
    content:     "";
    display:     block;
    padding-top: 100%; /* initial ratio of 1:1*/
}

.content {
    position: absolute;
    top:      0;
    left:     0;
    bottom:   0;
    right:    0;
}

</style>