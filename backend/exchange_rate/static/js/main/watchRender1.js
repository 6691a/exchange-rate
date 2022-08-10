const htmls = Vue.ref({})

async function getCurrency() {
    const res = []
    const el = document.getElementsByClassName('watch-list')
    for (const e of el) {
        const currency = e.href.split("/").pop()
        res.push(
            currency
        )
        htmls.value[currency] = 0
    }
    return res
}

function renderWatchList(currency) {
    const [price, fluctuation] = getFluctuation(currency.yester.standard_price, currency.last.standard_price)
    console.log("123")
    if (0 > price) {
        return `
        <strong class="text-primary">${price}원</strong>
        <strong class="text-primary">(${fluctuation}%)</strong>
        <h6 class="mt-1 mx-1 mb-0">${currency.last.standard_price.toFixed(float_digit)}원</h6>
        `
    }
    return `
    <strong class="text-danger">${price}원</strong>
    <strong class="text-danger">(${fluctuation}%)</strong>
    <h6 class="mt-1 mx-1 mb-0">${currency.last.standard_price.toFixed(float_digit)}원</h6>
    `
}

function addSocketEvent(socket) {
    socket.onmessage = (e) => {
        const res = JSON.parse(e.data)
        const data = res.data
        const yester = data.yester_exchange
        const last = data.last_exchange
        htmls.value[last.currency] = renderWatchList({ yester, last })
    }
}

async function socketConnect(name) {
    const protocol = (window.location.protocol === 'https:' ? 'wss' : 'ws') + '://'
    const socketPath = protocol + window.location.host + '/ws/watch/'
    const socket = new WebSocket(
        socketPath + name + '/'
    )

    addSocketEvent(socket)

}


const watchRenderFuncs = {
    getCurrency,
    renderWatchList,
    socketConnect,
}

const watchRenderVars = {
    htmls,
}

export {watchRenderFuncs, watchRenderVars}

