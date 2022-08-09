import backMenuFuncs from "../../../../static/js/back-menu.js";
import watchFuncs from "./watch.js";

const indexVue = Vue.createApp({
    setup() {
        return {
            backMenuFuncs,
            watchFuncs
        }
    }

})
indexVue.mount('#index')
