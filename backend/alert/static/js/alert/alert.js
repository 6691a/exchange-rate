let isClick = false

const alertHtml = Vue.ref()
const lastPath = window.location.pathname.split("/").pop().toUpperCase()
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

async function delAlert() {
    const res = await http.delete(
        "alert/",
        {
            data: {
                "currency": lastPath,
            }
        }

    )
    if (res.status !== 204) {
        // 실패 안내 출력
    }
    alertHtml.value = `<a href="/alert/${lastPath}" className="text-primary">설정하기</a>`

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
    alertHtml,
}
const alertFuncs = {
    alertKeyInputEvent,
    alertSubmit,
    delAlert,
}
export  {alertFuncs, alertVars}
