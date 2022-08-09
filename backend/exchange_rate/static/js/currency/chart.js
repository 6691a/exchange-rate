if (isDarkStyle) {
    let axisColor = config.colors_dark.axisColor;
    let bgColor = config.colors_dark.cardColor;

} else {
    let axisColor = config.colors.axisColor;
    let bgColor = config.colors.white;
}

const fluctuation = `0원 (0%)`
const price = 0
const apexChart = null
const series = Vue.ref([{
    name: '가격',
    data: [],
}])
const minWidth = window.innerWidth <= 500 ? 33 : 13

const chartVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            fluctuation: `0원 (0%)`,
            price: Vue.ref(0),
            apexChart: null,
            series: Vue.ref([{
                name: '가격',
                data: [],
            }]),
            minWidth: window.innerWidth <= 500 ? 33 : 13,
        }
    },
    methods: {
        renderChart() {
            const chartEl = document.querySelector('#chartEl')
            const chartConfig = {
                series: this.series,
                chart: {
                    height: "225",
                    width: "100%",
                    parentHeightOffset: 0,
                    parentWidthOffset: 0,
                    zoom: {
                        enabled: false
                    },
                    type: 'line',
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
                        top: 0,
                        right: 25,
                        bottom: 0,
                        left: 0
                    },
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
                        },
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
                        },
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
        },
        socketConnect(name) {
            const protocol = (window.location.protocol === 'https:' ? 'wss' : 'ws') + '://'
            const socketPath = protocol + window.location.host + '/ws/exchange_rate/'

            const socket = new WebSocket(
                socketPath + name + '/'
            )
            this.addSocketEvent(socket)
        },
        render_price(current_price, closing_price) {
            const [price, fluctuation] = getFluctuation(closing_price, current_price)

            if (0 > price) {
                return `
                <small class="text-primary">${price}원 (${fluctuation}%)</small>
                `
            }
            return `
            <small class="text-danger">${price}원 (${fluctuation}%)</small>
            `
        },
        addSocketEvent(socket) {
            socket.onmessage = (e) => {
                const res = JSON.parse(e.data)
                const data = res.data
                const exchange = data.exchange_rate
                const chartLength = data.chart_length
                const hight_price = data.hight_price
                const low_price = data.low_price
                const closing = data.closing_price
                const current_price = exchange.slice(-1)[0]["standard_price"]

                this.price = `${current_price}원`
                this.fluctuation = this.render_price(current_price, closing.standard_price)

                exchange.forEach((v) => this.series[0].data.push({ x: v.created_at, y: v.standard_price }))
                apexChart.updateSeries(this.series)
                apexChart.updateOptions({
                    chart: {
                        width: (() => `${Math.max(this.minWidth, Math.min(this.series[0].data.length / chartLength * 100, 100))}%`)()
                    },
                    markers: {
                        size: 6,
                        colors: 'transparent',
                        strokeColors: 'transparent',
                        strokeWidth: 4,
                        discrete: [{
                            fillColor: config.colors.white,
                            seriesIndex: 0,
                            dataPointIndex: this.series[0].data.length - 1,
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
                                    offsetY: -10,
                                    fillColor: config.colors.primary,
                                    strokeColor: config.colors.primary,
                                    strokeWidth: 2,
                                    size: 2,
                                },
                                label: {
                                    borderWidth: 0,
                                    borderRadius: 0,
                                    offsetX: 0,
                                    offsetY: -3,
                                    opacity: 1,
                                    style: {
                                        color: axisColor,
                                        background: bgColor,
                                        fontSize: '13px',
                                    },
                                    text: `${hight_price.standard_price}원`,
                                }
                            },
                            {
                                x: low_price.created_at,
                                y: low_price.standard_price,
                                marker: {
                                    offsetX: 0,
                                    offsetY: 10,
                                    fillColor: config.colors.primary,
                                    strokeColor: config.colors.primary,
                                    strokeWidth: 2,
                                    size: 2,
                                },
                                label: {
                                    borderWidth: 0,
                                    borderRadius: 0,
                                    offsetX: 0,
                                    offsetY: 43,
                                    style: {
                                        color: axisColor,
                                        background: bgColor,
                                        fontSize: '13px',
                                    },
                                    text: `${low_price.standard_price}원`,
                                }
                            },
                        ]
                    },
                })
            };
        }
    },

    mounted() {
        this.renderChart()
        const group = window.location.pathname.split("/").pop()
        this.socketConnect(group)
    },
})
// chartVue.mount('#chart')
