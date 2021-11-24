<template>
    <div>
        <container class='ProjectOverview'>
            <p class='header'>Project Overzicht</p>
        </container>
        <container class='RightSideProject'>
            <container class='ProjectAnnouncements'>
                 <p class = 'header'>Project Mededelingen</p>
            </container>
            <container class ='ProjectChat'>
                
            </container>
        </container>
    </div>
</template>

<script>
export default {
  components: {},
  name: "Project",
  data: function () {
    return {
    };
  },
 created(){
     this.$emit('loaded', 'Project')
 }
};
</script>
<style>
.ProjectOverview{
    width: 64vw;
    height: 84vh;
    margin: 1.25vw;
    display:inline-block;
}
.RightSideProject{
    width: 30vw;
    height: 84vh;
    margin: 1.25vw;
    display:inline-block;
}
.ProjectAnnouncements{
    width: 100%;
}
.ProjectChat{
    width: 100%;
}
.header{
    width: 100%;
    height: auto;
    background-color: #28418a;
    color: white;
    font-size: 4vh;
    font-family: Montserrat;
    padding-left: 1vw;
}

</style>