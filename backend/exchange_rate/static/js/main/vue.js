import {watchRenderFuncs, watchRenderVars} from "./watchRender.js";

const indexVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    setup() {
        return {
            watchRenderFuncs,
            watchRenderVars,
        }
    },
    mounted() {
        const currency = watchRenderFuncs.getCurrency()
        for (let c of currency) {
            watchRenderFuncs.socketConnect(c)
        }
    }

})
indexVue.mount('#index')
