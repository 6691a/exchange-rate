const lastPath = window.location.pathname.split("/").pop().toUpperCase()
let isClick = false
const nonLikeCss = "bx bxs-bell bx-sm silver"
const likeCss = "bx bxs-bell bx-sm yellow"
const input = Vue.ref()

async function addAlert(price){
    const res = await http.post(
        "alert/",
        {
            "currency": lastPath,
            price,
        }
    )
    if (res.status !== 200) {
        // 실패 안내 출력
        return false
    }
    return true
}

async function alertEvent(event) {
    // if (event.target.classList.contains("silver")) {
    const form = new bootstrap.Modal(document.getElementById('alertForm'))
    form.show()
    // }
    // else{
    //
    // }
}

function alertKeyInputEvent(event) {
    let keyCode = event.keyCode
    if ((keyCode > 31 && (keyCode < 48 || keyCode > 57)) && keyCode !== 46) {
        event.preventDefault();
    }
    let inputValue = event.target.value

    event.target.value = comma(uncomma(inputValue))
}
async function alertSubmit(event) {
    if (isClick || !input.value) {
        return;
    }
    isClick = true

    const value = uncomma(input.value)

    if (await addAlert(value)) {
        location.href = `/${lastPath}`
    }
    setTimeout(() => {
        isClick = false
    }, 500)
}
function comma(str) {
 str = String(str);
 return str.replace(/(\d)(?=(?:\d{3})+(?!\d))/g, '$1,');
}

function uncomma(str) {
 str = String(str);
 return str.replace(/[^\d]+/g, '');
}

const alertVars = {
    input,
}
const alertFuncs = {
    alertKeyInputEvent,
    alertSubmit,
    alertEvent
}
export  {alertFuncs, alertVars}
