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
        let chartLength = 0
        let chart = null
        let res = null
        const currency = Vue.ref()

        const getExchangeRate = async (currency) => {
            const r = await axios.get(api_host, {
                params: {
                    currency
                }
            })
            if (r.status === 200) {
                data = r.data.data
                chartLength = data.chart_length
                price.value = data.exchange_rate.slice(-1)[0]["standard_price"]

                return data
            }
        }

        const renderChart = () => {
            const chartEl = document.querySelector('#chartEl')
            // const data = res.exchange_rate
            const chartConfig = {
                series: [],
                // series: [{
                //     name: "가격",
                //     data: data.map((v) => ({ x: v.created_at, y: v.standard_price }))
                // }],
                chart: {
                    height: "225",
                    width: "100%",
                    // width: (() => `${Math.max(6, Math.min(data.length / chartLength * 100, 100))}%`)(),
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
                markers: {
                    size: 6,
                    colors: 'transparent',
                    strokeColors: 'transparent',
                    strokeWidth: 4,
                    discrete: [{
                        fillColor: config.colors.white,
                        seriesIndex: 0,
                        // dataPointIndex: data.length - 1,
                        dataPointIndex: 0,
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
                annotations: {
                    points: [
                        {
                            x: new Date('12:51').getTime(),
                            y: 1272.9,
                            marker: {
                                size: 8,
                            },
                            label: {
                                borderColor: '#FF4560',
                                text: 'Point Annotation'
                            }
                        }
                    ],
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
                chart = new ApexCharts(chartEl, chartConfig);
                chart.render();
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
                const data = JSON.parse(e.data);
                // Object.assign(obj1, obj2)
                console.log(data)
                res = data
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


