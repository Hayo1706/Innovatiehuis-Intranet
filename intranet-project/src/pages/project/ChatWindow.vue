<template>
    <div>
        <div class="component-container">
            <div class="component-header">
                Project Chat
            </div>
        </div>
        <div class="component-body">
            <div class="container-fluid">
                <div class="row" v-for="message in messages" :key="message.name">
                    {{message.first_name}} {{message.last_name}}: {{ message.content }}
                </div>
            </div>
            <div>
                <div class="input-group">
                    <input
                    id="search-input"
                    type="search"
                    class="form-control"
                    placeholder="Type je bericht..."
                    v-model="typeField"
                    />
                    <button @click="addMessage(typeField)">
                    Verzenden
                    </button>
                </div>
                
            </div>
        </div>
    </div>

</template>

<script>
import ChatMessage from "./ChatMessage.vue";
export default {
    name: "ChatWindow",
    component: [ChatMessage],
    data: function () {
        return { 
            messages: [
                {first_name: "John", last_name: "Doe", content: "Hey"},
                {first_name: "John", last_name: "Doe", content: "Does this work?"},
                {first_name: "Jane", last_name: "Doe", content: "Heya!! Yes it works"},
                {first_name: "John", last_name: "Doe", content: "Alright awesome!"},
            ],
        };
    },
    methods: {
        addMessage(newMessage){
            if(newMessage != null){
                this.messages.push({name: "Test", message: newMessage})
            }
            
            this.typeField = null;
        }
    }
}
</script>
<style scoped>
#username{
}
</style>
