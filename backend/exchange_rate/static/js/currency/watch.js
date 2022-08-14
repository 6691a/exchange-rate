let isClick = false
const nonLikeCss = "bx bxs-heart bx-sm silver"
const likeCss = "bx bxs-heart bx-sm light-red"
const lastPath = window.location.pathname.split("/").pop().toUpperCase()


async function addWatchList() {
    const res = await http.post(
        "watch/",
        {
            "currency": lastPath
        }
    )
    if (res.status !== 200) {
        // 실패 안내 출력
    }
}

async function delWatchList() {
    const res = await http.delete(
        "watch/",
        {
            data: {
                "currency":  lastPath
            }
        }
    )
    if (res.status !== 204) {
        // 실패 안내 출력
    }
}
async function setHeart(event) {
    if (isClick) {
        return;
    }
    isClick = true;

    if (event.target.classList.contains("silver")) {
        event.target.className = likeCss
        await addWatchList()
    }
    else {
        event.target.className =  nonLikeCss
        await delWatchList()
    }

    setTimeout(() => {
        isClick = false;
    }, 500);
}


const watchFuncs = {
    setHeart,
}


export default watchFuncs

