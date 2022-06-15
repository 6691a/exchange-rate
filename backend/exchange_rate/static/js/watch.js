const watchVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            watch_length: 0,
            watchList: [],
            currencyList: {},
        }
    },
    methods: {
        socketConnect: function (name) {
            const protocol = (window.location.protocol === 'https:' ? 'wss' : 'ws') + '://'
            const socketPath = protocol + window.location.host + '/ws/watch/'
            const socket = new WebSocket(
                socketPath + name + '/'
            )
            this.addSocketEvent(socket)
        },
        addSocketEvent: function (socket) {
            socket.onmessage = (e) => {
                const res = JSON.parse(e.data)
                console.log(res)
                const data = res.data
                // console.log(data.last_exchange); 
                // console.log(data.first_exchange); 
                const first = data.first_exchange
                const last = data.last_exchange

                this.currencyList[first.currency] = {
                    first,
                    last
                }
                console.log(this.currencyList);
            }
        },
    },
    async created() {
        const res = await http.get("watch")
        if (res.status !== 200) {
            return
        }

        this.watchList = res.data.data
        this.watch_length = this.watchList.length

        for (let i of this.watchList) {
            this.socketConnect(i.currency)
        }
    },
    // [[this.currencyList[w.currency].first.standard_price]]
    // [[this.currencyList[w.currency].last.standard_price]]
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
                                <span class="text-muted">10%</span>
                                <h6 class="mt-1 mb-0"> [[ this.currencyList[w.currency].last.standard_price ]]원</h6>
                            </div>
                        </div>
                    </div>
                </li>
            </a>
        </ul>
    </div> 
    `,

})
watchVue.mount('#watch')

