let axisColor
if (isDarkStyle) {
    axisColor = config.colors_dark.axisColor;
} else {
    axisColor = config.colors.axisColor;
}

const chartVue = Vue.createApp({
    delimiters: ['[[', ']]'],

    setup() {
        let price = Vue.ref(0)
        let apexChart = null
        const currency = Vue.ref()

        const renderChart = () => {
            const chartEl = document.querySelector('#chartEl')
            const chartConfig = {
                series: [],
                chart: {
                    height: "225",
                    width: "100%",
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
                    },
                    animations: {
                        enabled: false,
                        easing: "linear",
                        dynamicAnimation: {
                            speed: 1000
                        }
                    },
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
                grid: {
                    show: false,
                    padding: {
                        top: -10,
                        left: 0,
                        right: 10,
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
                            colors: axisColor
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
                noData: {
                    text: '잠시만 기다려 주세요 😅',
                    style: {
                        color: axisColor,
                        fontSize: '13px',
                    }
                }

            }
            if (typeof chartEl !== undefined && chartConfig !== null) {
                apexChart = new ApexCharts(chartEl, chartConfig);
                apexChart.render();
            }
        }

        const socketConnect = (name) => {
            const protocol = (window.location.protocol === 'https:' ? 'wss' : 'ws') + '://'
            const socketPath = protocol + window.location.host + '/ws/exchange_rate/'

            const socket = new WebSocket(
                socketPath + name + '/'
            )
            // else if (socket.url.indexOf(name) === -1) {
            //     socket.close()
            //     socket = new WebSocket(
            //         p + name + '/'
            //     )
            // }

            addSocketEvent(socket)
        }

        const addSocketEvent = (socket) => {

            socket.onmessage = (e) => {
                const res = JSON.parse(e.data)
                const data = res.data

                console.log(data)
                // price.value = data.exchange_rate.slice(-1)[0]["standard_price"]

                apexChart.updateSeries([{
                    name: '가격',
                    data: data.map((v) => ({ x: v.created_at, y: v.standard_price })),
                }])
                console.log(data.length)
                apexChart.updateOptions({
                    width: (() => `${Math.max(6, Math.min(data.length / chartLength * 100, 100))}%`)(),
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
                })
            };
        }


        Vue.onMounted(async () => {
            renderChart()
            const group = currency.value.getAttribute("value")
            socketConnect(group)
            // const res = await getExchangeRate(currency.value.textContent)

        })
        return { currency, price }
    },
})
chartVue.mount('#chart')


