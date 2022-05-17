// 
// let socket
// const protocol = (window.location.protocol === 'https:' ? 'wss' : 'ws') + '://'
// const path = protocol + window.location.host + '/ws/exchange_rate/'

// function socket_connect(name) {
//     if (!socket) {
//         socket = new WebSocket(
//             path + name + '/'
//         )
//     }
//     else if (socket.url.indexOf(name) === -1) {
//         socket.close()
//         socket = new WebSocket(
//             path + name + '/'
//         )
//     }
//     add_socket_event()

// }
// function add_socket_event() {
//     socket.onmessage = function (e) {
//         const data = JSON.parse(e.data);
//         console.log(data)
//     };
// }

// document.querySelector('#socket_1').onclick = function (e) {
//     socket_connect(this.value)
// }
// document.querySelector('#socket_2').onclick = function (e) {
//     socket_connect(this.value)
// }
const res = {}
const chart = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            res
        }
    },
    methods: {
        getExchangeRate: async (currency) => {
            const r = await axios.get(api_host, {
                params: {
                    currency
                }
            })
            if (r.status === 200) {
                this.res = r.data.data
            }
        },
        renderChart: () => {
            const totalBalanceChartEl = document.querySelector('#totalBalanceChart')
            const data = self.res.exchange_rate
            const totalBalanceChartConfig = {
                series: [{
                    name: "가격",
                    data: data.map((v) => ({ x: v.created_at, y: v.standard_price }))
                }],
                chart: {
                    height: 225,
                    parentHeightOffset: 0,
                    parentWidthOffset: 0,
                    zoom: { enabled: false },
                    type: 'line',
                    dropShadow: {
                        enabled: false,
                        top: 10,
                        left: 5,
                        blur: 3,
                        color: config.colors.primary,
                        opacity: 0.15
                    },
                    toolbar: {
                        show: false
                    }
                },
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    width: 3,
                    curve: 'smooth'
                },
                legend: {
                    show: false
                },
                colors: [config.colors.primary],
                markers: {
                    size: 6,
                    colors: 'transparent',
                    strokeColors: 'transparent',
                    strokeWidth: 4,
                    discrete: [{
                        fillColor: config.colors.white,
                        seriesIndex: 0,
                        dataPointIndex: data.length - 1,
                        strokeColor: config.colors.primary,
                        strokeWidth: 8,
                        size: 6,
                        radius: 8,
                    },],
                    hover: {
                        size: 7
                    }
                },
                grid: {
                    show: false,
                    padding: {
                        top: -10,
                        left: 0,
                        right: 20,
                        bottom: 10
                    }
                },
                xaxis: {
                    axisBorder: {
                        show: false
                    },
                    axisTicks: {
                        show: false
                    },
                    labels: {
                        show: false,
                        style: {
                            fontSize: '13px',
                            colors: self.axisColor
                        }
                    },
                    tooltip: {
                        enabled: false
                    }
                },
                yaxis: {
                    labels: {
                        show: false
                    },

                },
                points: [
                    {
                        x: new Date('01 Dec 2017').getTime(),
                        y: 8607.55,
                        marker: {
                            size: 8,
                        },
                        label: {
                            borderColor: '#FF4560',
                            text: 'Point Annotation'
                        }
                    }
                ]
            }
            if (typeof totalBalanceChartEl !== undefined && totalBalanceChartEl !== null) {
                const totalBalanceChart = new ApexCharts(totalBalanceChartEl, totalBalanceChartConfig);
                totalBalanceChart.render();
            }
        }
    },
    async mounted() {

        await this.getExchangeRate(this.$refs.currency.textContent);
        this.renderChart()
    }
})
chart.mount('#chart')
