let axisColor
let bgColor


if (isDarkStyle) {
    axisColor = config.colors_dark.axisColor
    bgColor = config.colors_dark.cardColor
} else {
    axisColor = config.colors.axisColor
    bgColor = config.colors.white
}


let fluctuation = Vue.ref(`0원 (0%)`)
let price = Vue.ref(`0원`)
const series = [{
    name: '가격',
    data: [],
}]
const minWidth = window.innerWidth <= 500 ? 33 : 13

async function get_exchange_rate(currency) {
    const res = await http.get(
        "/",
        {
            params: {
                currency
            }
        }
    )

    if (res.status !== 200) {
        // 실패 안내 출력
    }
    return res
}

function renderChart(series, apexChart) {
    const chartEl = document.querySelector('#chartEl')
    const chartConfig = {
        series,
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
                bottom: 10,
                left: 5
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
        apexChart.value = new ApexCharts(chartEl, chartConfig);

        apexChart.value.render();
    }

}

function socketConnect(currency) {
    const protocol = (window.location.protocol === 'https:' ? 'wss' : 'ws') + '://'
    const socketPath = protocol + window.location.host + '/ws/exchange_rate/'

    const socket = new WebSocket(
        socketPath + currency + '/'
    )
    addSocketEvent(socket)
}

function render_price(current_price, closing_price) {
    const [price, fluctuation] = getFluctuation(closing_price, current_price)

    if (0 > price) {
        return `
        <small class="text-primary">${price}원 (${fluctuation}%)</small>
        `
    }
    return `
    <small class="text-danger">${price}원 (${fluctuation}%)</small>
    `
}

function addSocketEvent(socket) {
    socket.onmessage = (e) => {
        const res = JSON.parse(e.data)
        const data = res.data
        const exchange = data.exchange_rate
        const chartLength = data.chart_length
        const hight_price = data.hight_price
        const low_price = data.low_price
        const closing = data.closing_price
        const current_price = exchange.slice(-1)[0]["standard_price"]

        //
        price.value = `${current_price}원`
        fluctuation.value = render_price(current_price, closing.standard_price)
        //
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

const chartVars = {
    price,
    fluctuation

}
const chartFuncs = {
    get_exchange_rate,
    renderChart,
    socketConnect,
}


export  {chartVars, chartFuncs}
