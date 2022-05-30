let axisColor
if (isDarkStyle) {
    axisColor = config.colors_dark.axisColor;
    bgColor = config.colors_dark.cardColor;

} else {
    axisColor = config.colors.axisColor;
    bgColor = config.colors.white;
}

const chartVue = Vue.createApp({
    delimiters: ['[[', ']]'],

    setup() {
        let price = Vue.ref(0)
        let apexChart = null
        let series = [{
            name: '가격',
            data: [],
        }]
        const currency = Vue.ref()
        const minWidth = window.innerWidth <= 500 ? 35 : 10

        const renderChart = () => {
            const chartEl = document.querySelector('#chartEl')
            const chartConfig = {
                series: [],
                chart: {
                    height: "225",
                    width: "100%",
                    parentHeightOffset: 0,
                    parentWidthOffset: 0,
                    zoom: {
                        enabled: false
                    },
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
                        left: 20,
                        right: 35,
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
                        show: true,
                        style: {
                            fontSize: '1px',
                            colors: bgColor
                        }
                    },
                    tooltip: {
                        enabled: false
                    }
                },
                yaxis: {
                    labels: {
                        show: true,
                        style: {
                            fontSize: '1px',
                            colors: bgColor
                        }
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
                const exchange = data.exchange_rate
                const chartLength = data.chart_length
                const hight_price = data.hight_price
                const low_price = data.low_price
                price.value = exchange.slice(-1)[0]["standard_price"]
                exchange.forEach((v) => series[0].data.push({ x: v.created_at, y: v.standard_price }))
                apexChart.updateSeries(series)
                apexChart.updateOptions({
                    chart: {
                        width: (() => `${Math.max(minWidth, Math.min(series[0].data.length / chartLength * 100, 100))}%`)()
                    },
                    markers: {
                        size: 6,
                        colors: 'transparent',
                        strokeColors: 'transparent',
                        strokeWidth: 4,
                        discrete: [{
                            fillColor: config.colors.white,
                            seriesIndex: 0,
                            dataPointIndex: series[0].data.length - 1,
                            strokeColor: config.colors.primary,
                            strokeWidth: 8,
                            size: 5,
                            radius: 8,
                        },],
                        hover: {
                            size: 7
                        }
                    },
                    annotations: {
                        points: [
                            {
                                x: hight_price.created_at,
                                y: hight_price.standard_price,
                                marker: {
                                    offsetX: 0,
                                    offsetY: -15,
                                    fillColor: config.colors.primary,
                                    strokeColor: config.colors.primary,
                                    strokeWidth: 2,
                                    size: 2,
                                },
                                label: {
                                    borderWidth: 0,
                                    borderRadius: 0,
                                    offsetX: 0,
                                    offsetY: -10,
                                    opacity: 1,
                                    style: {
                                        color: axisColor,
                                        background: bgColor,
                                        fontSize: '13px',
                                    },
                                    text: `최고 ${hight_price.standard_price}원`,

                                }
                            },
                            {
                                x: low_price.created_at,
                                y: low_price.standard_price,
                                marker: {
                                    offsetX: 0,
                                    offsetY: 15,
                                    fillColor: config.colors.primary,
                                    strokeColor: config.colors.primary,
                                    strokeWidth: 2,
                                    size: 2,
                                },
                                label: {
                                    borderWidth: 0,
                                    borderRadius: 0,
                                    offsetX: 0,
                                    offsetY: 50,
                                    style: {
                                        color: axisColor,
                                        background: bgColor,
                                        fontSize: '13px',
                                    },
                                    text: `최저 ${low_price.standard_price}원`,

                                }
                            },
                        ]
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


