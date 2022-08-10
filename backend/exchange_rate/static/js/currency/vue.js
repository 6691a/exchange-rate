import watchFuncs from "./watch.js";
import {chartFuncs, chartVars} from "./chart.js";

const indexVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    setup() {
        return {
            watchFuncs,
            chartVars,
        }
    },
    mounted() {
        chartFuncs.renderChart()
        chartFuncs.socketConnect(window.location.pathname.split("/").pop())
    },

})
indexVue.mount('#index')
