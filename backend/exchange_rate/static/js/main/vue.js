import {watchRenderFuncs, watchRenderVars} from "./watchRender1.js";

const indexVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    setup() {
        return {
            watchRenderFuncs,
            watchRenderVars,
        }
    },

    async mounted() {
        const currency = await watchRenderFuncs.getCurrency()
        for (let c of currency) {
            await watchRenderFuncs.socketConnect(c)
        }
    }

})
indexVue.mount('#index')
