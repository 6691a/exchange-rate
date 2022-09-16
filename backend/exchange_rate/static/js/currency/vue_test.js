import watchFuncs from "./watch.js";
import {chartFuncs, chartVars} from "./chart.js";
import {alertFuncs, alertVars} from "../../../static/js/alert/alert.js";


const indexVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    setup() {
        const currency = window.location.pathname.split("/").pop();
        const series = [{
            name: '가격',
            data: [],
        }];
        const apexChart = Vue.ref();
        Vue.onBeforeMount(async () => {
            const res = await chartFuncs.get_exchange_rate(currency)
            const exchange = res.data.data.exchange_rate
            exchange.forEach((v) => series[0].data.push({ x: v.created_at, y: v.standard_price }))
            apexChart.value.updateSeries(series)
        });
        Vue.onMounted(async () => {
            chartFuncs.renderChart(series, apexChart)

        });
        return {
            currency,
            series,
            apexChart,
            watchFuncs,
            alertFuncs,
            chartVars,
            alertVars,
        }
    },

})
indexVue.mount('#index')
