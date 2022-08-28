let data = []
let search_list

async function getCountry() {
    const res = await http.get("country/")
    if (res.status !== 200) {
        // 실패 안내 출력
    }
    const country= res.data.data
    for (const c of country) {
        const v = Object.values(c)
        data.push(v.slice(0,v.length -1).join(','))
    }
}
function template(text, path) {
    return `
    <ul class="my-1 p-0 m-0">
        <a href="/${path}" class="watch-list">
            <li class="btn d-flex px-0">
                <div class="avatar flex-shrink-0 me-3">
                    <img src="${static_host}static/img/currency/${path}.png" alt="User">
                </div>
                <div class="d-flex w-100 flex-wrap align-items-center justify-content-between gap-2">
                <div class="me-2">
                    <h6 class="mb-0">${text}</h6>
                </div>
            </li>
        </a>
    </ul>   
  
    `

}

function search(e) {
    const val = e.target.value
    if (!val) {
        search_list.innerHTML = ""
        return
    }
    const filterData = data.filter((text) => {
        const regex = new RegExp(val, 'gi')
        return text.match(regex)
    })
    if (filterData) {
        let html = ""
        console.log(data)
        filterData.map((data) => {
            const splits = data.split(",")
            html += template(splits[1], splits[0])
        })
        search_list.innerHTML = `
        <div class="col-xl-12">
            <div class="card h-100">
                <div class="card-body py-2">
                ${html}
                </div>
            </div>
        </div>
        `
    }

}

window.onload = async function(){
    await getCountry()

    search_list = document.getElementById("search_list")
    const searchElement = document.getElementById("search")

    searchElement.addEventListener("keyup", search)



}

