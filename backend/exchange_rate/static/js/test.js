const mainVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    // data() {
    //     return {
    //         counter: 1
    //     }
    // },

    methods: {
        async addWatch(currency) {
            console.log(currency)
            try {
                const r = await http.post("/watch", {
                    currency: currency
                })
                console.log(r.status)
            }
            catch (e) {
                console.log(e)
            }
        }
    }
})
mainVue.mount('#test')