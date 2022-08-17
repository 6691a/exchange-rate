import {alertVars, alertFuncs} from "./alert.js";


const indexVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    setup() {
        return {
            alertVars,
            alertFuncs
        }
    },
    mounted() {
    },

})
indexVue.mount('#index')
