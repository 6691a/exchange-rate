

function addAlert(){
    const res = await http.post("alert", { "currency": lastPath })
    if (res.status !== 200) {
        // 실패 안내 출력
    }
}

const alertFuncs = {
    addAlert,
}

export  {AlertFuncs}