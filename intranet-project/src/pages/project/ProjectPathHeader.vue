<template>
    <div>
        <text v-if="this.currentPath == ''">
            Bestandsoverzicht
        </text>
        <text v-else
            class="hover"
            @click="currentPathChanged('', this.projectID)">
            Home/                  
        </text>
        <span v-for="(path, index) in this.currentPath.split('/').slice(0,-1)" :key="path">
        <text
            class="hover"
            @click="currentPathChanged('/' + this.currentPath.split('/').slice(1, index+1)[0], this.projectID)"
            v-if="path != ''">{{path}}/
        </text>
        </span>
        <text>
            {{this.currentPath.split('/').slice(-1)[0]}}
        </text>
    </div>
</template>

<script>

export default {
    setup() {
        
    },
    name: "ProjectPathHeader",
    props: ['currentPath'],
};
</script>
