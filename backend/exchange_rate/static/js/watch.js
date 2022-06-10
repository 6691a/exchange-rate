const watchVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            watch_length: 0,
            watch: []
        }
    },
    methods: {
        click: function (e) {
            this.watch_length += 1
        }
    },
    async created() {
        const res = await http.get("watch")
        console.log(res)
        this.watch_length = 10
    },
    template: `
    <div class="card-header d-flex align-items-center ">
        <h5 class="card-title m-0 me-2">관심 목록</h5>
        <h6 class="text-muted d-block mb-1">[[watch_length]]개</h6>
    </div>
    `,
    // mounted() {
    //     console.log()
    //     this.items = [
    //         { message: 0 }, { message: 1 }
    //     ]
    // }
})
watchVue.mount('#watch')