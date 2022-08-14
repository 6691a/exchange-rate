const lastPath= window.location.pathname.split("/").pop().toUpperCase()
let isClick = false
const nonLikeCss = "bx bxs-bell bx-sm silver"
const likeCss = "bx bxs-bell bx-sm silver"

async function addAlert(){
    const res = await http.post(
        "alert/",
        {
            "currency": lastPath
        }
    )
    if (res.status !== 200) {
        // 실패 안내 출력
    }
}

async function setAlert(event) {
    if (isClick) {
        return;
    }
    isClick = true;
    if (event.target.classList.contains("silver")) {
        // event.target.className = likeCss
        await addAlert()
    }

    // const attr = clickAttribute
    // if (event.target.getAttribute(attr) === "true") {
    //     event.target.className =  nonLikeCss
    //     event.target.setAttribute(attr, "false")
    //     await watchFuncs.delWatchList()
    // } else {
    //     event.target.className = likeCss
    //     event.target.setAttribute(attr, "true")
    //     await watchFuncs.addWatchList()
    // }

    setTimeout(() => {
        isClick = false;
    }, 500);
}

const alertFuncs = {
    setAlert,
}
export default alertFuncs
