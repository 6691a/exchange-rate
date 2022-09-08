import watchFuncs from "./watch.js";
import {chartFuncs, chartVars} from "./chart.js";
import {alertFuncs, alertVars} from "../../../static/js/alert/alert.js";


const indexVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    setup() {
        return {
            watchFuncs,
            alertFuncs,
            chartVars,
            alertVars,
        }
    },
    mounted() {
        chartFuncs.renderChart()
        chartFuncs.socketConnect(window.location.pathname.split("/").pop())
    },

})
indexVue.mount('#index')