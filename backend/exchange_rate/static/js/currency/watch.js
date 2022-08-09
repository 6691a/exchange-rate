let watchListClick = false
const clickAttribute= "data-watch"
const nonLikeCss= "bx bxs-heart bx-sm silver"
const likeCss= "bx bxs-heart bx-sm light-red"
const lastPath= window.location.pathname.split("/").pop()


async function addWatchList() {
    const res = await http.post("watch", { "currency": lastPath })
    if (res.status !== 200) {
        // Modal 안내 출력
    }
}

async function delWatchList() {
    const res = await http.delete("watch", {data: {"currency":  lastPath}})
    if (res.status !== 204) {
        // Modal 안내 출력
    }
}
async function setHeart(event) {
    if (watchListClick) {
        return;
    }
    const attr = clickAttribute
    if (event.target.getAttribute(attr) === "true") {
        event.target.className =  nonLikeCss
        event.target.setAttribute(attr, "false")
        await watchFuncs.delWatchList()
    } else {
        event.target.className = likeCss
        event.target.setAttribute(attr, "true")
        await watchFuncs.addWatchList()
    }
    watchListClick = true;

    setTimeout(() => {
        watchListClick = false;
    }, 500);
}


const watchFuncs = {
    addWatchList,
    delWatchList,
    setHeart,
}


export default watchFuncs
// const watchVue = Vue.createApp({
//     delimiters: ['[[', ']]'],
//     methods: {
//         async addWatchList() {
//             res = await http.post("watch", { "currency": this.lastPath })
//             if (res.status != 200) {
//                 // Modal 안내 출력
//             }
//         },
//         async delWatchList() {
//             res = await http.delete("watch", { data: { "currency": this.lastPath } })
//             if (res.status != 204) {
//                 // Modal 안내 출력
//             }
//         },
//         async setHeart(event) {
//             if (this.watchListClick) {
//                 return;
//             }
//             if (event.target.getAttribute(this.clickAttribute) === "true") {
//                 event.target.className = this.nonLikeCss
//                 event.target.setAttribute(this.clickAttribute, "false")
//                 this.delWatchList()
//             }
//             else {
//                 event.target.className = this.likeCss
//                 event.target.setAttribute(this.clickAttribute, "true")
//                 this.addWatchList()
//             }
//             this.watchListClick = true;
//
//             setTimeout(() => {
//                 this.watchListClick = false;
//             }, 500);
//         },
//     },
// })
// watchVue.mount('#watch')
//
