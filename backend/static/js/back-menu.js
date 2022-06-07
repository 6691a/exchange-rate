const backmenuVue = Vue.createApp({
    delimiters: ['[[', ']]'],
    // data() {
    //     return {
    //         counter: 1
    //     }
    // },

    methods: {
        back(currency) {
            window.history.back();
        }
    }
})
backmenuVue.mount('#back-menu')