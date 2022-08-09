import backMenuFuncs from "../../../../static/js/back-menu.js";
import watchFuncs from "./watch.js";
import {chartFuncs, chartVars} from "./chart.js";

const indexVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    setup() {
        return {
            backMenuFuncs,
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
