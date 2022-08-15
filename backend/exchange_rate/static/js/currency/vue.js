import watchFuncs from "./watch.js";
import {chartFuncs, chartVars} from "./chart.js";
import alertFuncs from "../../../static/js/alert.js";


const indexVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    setup() {
        return {
            watchFuncs,
            alertFuncs,
            chartVars,
        }
    },
    mounted() {
        chartFuncs.renderChart()
        chartFuncs.socketConnect(window.location.pathname.split("/").pop())
    },

})
indexVue.mount('#index')
