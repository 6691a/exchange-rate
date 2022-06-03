const chartVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    // data() {
    //     return {
    //         counter: 1
    //     }
    // },

    methods: {
        async addWatch() {
            try {
                const r = await http.post("/watch", {
                    currency: 'veneas'
                })
                console.log(r.status)
            }
            catch (e) {
                console.log(e)
            }


        }
    }
})
chartVue.mount('#test')