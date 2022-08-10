const watchRenderVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            watch_length: 0,
            watchList: [],
            currencyList: {},
        }
    },
    methods: {
        async getWatchList(options) {
            const res = await http.get("watch")
            if (res.status !== 200) {
                return
            }
            this.watchList = res.data.data
            this.watch_length = this.watchList.length
        },

        async addWatchList() {
            res = await http.post("watch", { "currency": this.lastPath })
            if (res.status != 200) {
                // Modal 안내 출력
            }
        },

        async delWatchList() {
            res = await http.delete("watch", { data: { "currency": this.lastPath } })
            if (res.status != 204) {
                // Modal 안내 출력
            }
        },

        async setHeart(event) {
            if (this.watchListClick) {
                return;
            }
            if (event.target.getAttribute(this.clickAttribute) === "true") {
                event.target.className = this.nonLikeCss
                event.target.setAttribute(this.clickAttribute, "false")
                this.delWatchList()
            }
            else {
                event.target.className = this.likeCss
                event.target.setAttribute(this.clickAttribute, "true")
                this.addWatchList()
            }
            this.watchListClick = true;

            setTimeout(() => {
                this.watchListClick = false;
            }, 500);
        },

        renderWatchList(currency) {
            const [price, fluctuation] = getFluctuation(currency.yester.standard_price, currency.last.standard_price)

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

        },
        socketConnect(name) {
            const protocol = (window.location.protocol === 'https:' ? 'wss' : 'ws') + '://'
            const socketPath = protocol + window.location.host + '/ws/watch/'
            const socket = new WebSocket(
                socketPath + name + '/'
            )
            this.addSocketEvent(socket)
        },
        addSocketEvent(socket) {
            socket.onmessage = (e) => {
                const res = JSON.parse(e.data)
                console.log(res)
                const data = res.data
                const yester = data.yester_exchange
                const last = data.last_exchange

                this.currencyList[last.currency] = {
                    yester,
                    last
                }
            }
        },
    },
    async mounted() {
        await this.getWatchList()

        for (let i of this.watchList) {
            this.socketConnect(i.currency)
        }
    },

    template: `
    <div class="card-header d-flex align-items-center ">
        <h5 class="card-title m-0 me-2">관심 목록</h5>
        <h6 class="text-muted d-block mb-1">[[watch_length]]개</h6>
    </div>
    <div class="card-body">
        <ul class="p-0 m-0">
            <a v-for="w in watchList" v-bind:href="'${host}/' + w.currency" v-bind:data-currency=w.currency >
                <li class="btn d-flex mb-4 px-0">
                    <div class="avatar flex-shrink-0 me-3">
                        <img v-bind:src="'${static_host}${assetsPath}/img/currency/' + w.currency.toLowerCase() + '.png'" /> 
                    </div>
                    <div class="d-flex w-100 flex-wrap align-items-center justify-content-between gap-2">
                        <div class="me-2">
                            <h6 class="mb-0">[[ w.name ]]</h6>
                        </div>
                        <div class="user-progress d-flex align-items-center gap-1">
                            <div>
                                <template v-if="currencyList[w.currency]">
                                    <div v-html="renderWatchList(currencyList[w.currency])"></div>
                                </template>
                                <template v-else>
                                    <strong class="text-muted">0원</strong>
                                    <strong class="text-muted">(0%)</strong>
                                    <h6 class="mt-1 mb-0">0원</h6>
                                </template>
                            </div>
                        </div>
                    </div>
                </li>
            </a>
        </ul>
    </div> 
    `,

})
watchRenderVue.mount('#watch-render')

