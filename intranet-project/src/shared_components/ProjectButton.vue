<template>
  <button @click="onClick()" id="project-button">
    <img
      v-if="dateStringtoJsDate(lastUpdated) >= lastVisit"
      src=".\..\assets\images\logo\square.png"
    />
    <img
      v-if="dateStringtoJsDate(lastUpdated) < lastVisit"
      src=".\..\assets\images\logo\square_dark.png"
    />
    {{ this.projectName }}
  </button>
</template>

<script>
export default {
  name: "AnnouncementWindow",
  props: ["projectId", "projectName", "lastUpdated"],
  data: function () {
    return {
      lastVisit: new Date()
    };
  },
  methods: {
    onClick() {
      this.$router.push("/project/" + this.projectId);
    },
    dateStringtoJsDate(sqlDate){ // TODO: Move to service class
        //sqlDate in SQL DATETIME format ("yyyy-mm-dd hh:mm:ss.ms")
        var sqlDateArr1 = sqlDate.split("-");
        //format of sqlDateArr1[] = ['yyyy','mm','dd hh:mm:ms']
        var sYear = sqlDateArr1[0];
        var sMonth = (Number(sqlDateArr1[1]) - 1).toString();
        var sqlDateArr2 = sqlDateArr1[2].split(" ");
        //format of sqlDateArr2[] = ['dd', 'hh:mm:ss.ms']
        var sDay = sqlDateArr2[0];
        var sqlDateArr3 = sqlDateArr2[1].split(":");
        //format of sqlDateArr3[] = ['hh','mm','ss.ms']
        var sHour = sqlDateArr3[0];
        var sMinute = sqlDateArr3[1];
        var sqlDateArr4 = sqlDateArr3[2].split(".");
        //format of sqlDateArr4[] = ['ss','ms']
        var sSecond = sqlDateArr4[0];
        var sMillisecond = '000';
        
        var date = new Date(sYear,sMonth,sDay,sHour,sMinute,sSecond,sMillisecond);

        return date;
    }
  },
};
</script>


<style scoped>
#project-button {
  font-size: 16pt;
  font-weight: bold;
  background-color: var(--gold2);
  color: var(--blue1);
  width: 300px;
  height: 60px;
  border-style: outset;
  align-items: center;
  display: flex;
  border-radius: 8px;
}
img {
  height: 5vh;
  padding-right: 8px;
  cursor: pointer;
}
</style>