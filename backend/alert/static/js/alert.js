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
    else {

    }
    setTimeout(() => {
        isClick = false;
    }, 500);
}

function alertKeyInputEvent(event) {
    let keyCode = event.keyCode
    if ((keyCode > 31 && (keyCode < 48 || keyCode > 57)) && keyCode !== 46) {
        event.preventDefault();
    }
    let inputValue = event.target.value

    event.target.value = comma(uncomma(inputValue))
}

function comma(str) {
 str = String(str);
 return str.replace(/(\d)(?=(?:\d{3})+(?!\d))/g, '$1,');
}

function uncomma(str) {
 str = String(str);
 return str.replace(/[^\d]+/g, '');
}
const alertFuncs = {
    setAlert,
    alertKeyInputEvent
}
export default alertFuncs
