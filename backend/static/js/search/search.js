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

function template(text) {
    return `
   <div class="col-xl-12"><!-- Transactions --><div class="card h-100"><div class="card-header d-flex align-items-center"><h5 class="card-title m-0 me-2">관심 목록</h5><h6 class="text-muted d-block mb-1">2개</h6></div><div class="card-body"><ul class="p-0 m-0"><a href="/USD" class="watch-list"><li class="btn d-flex mb-4 px-0"><div class="avatar flex-shrink-0 me-3"><img src="/static/img/currency/usd.png" alt="User"></div><div class="d-flex w-100 flex-wrap align-items-center justify-content-between gap-2"><div class="me-2"><h6 class="mb-0">미국</h6></div><div class="user-progress d-flex align-items-center gap-1"><div>
        <strong class="text-primary">-4.50원</strong>
        <strong class="text-primary">(-0.34%)</strong>
        <h6 class="mt-1 mx-1 mb-0">1333.00원</h6>
        </div></div></div></li></a><a href="/JPY" class="watch-list"><li class="btn d-flex mb-4 px-0"><div class="avatar flex-shrink-0 me-3"><img src="/static/img/currency/jpy.png" alt="User"></div><div class="d-flex w-100 flex-wrap align-items-center justify-content-between gap-2"><div class="me-2"><h6 class="mb-0">일본</h6></div><div class="user-progress d-flex align-items-center gap-1"><div>
        <strong class="text-primary">-5.72원</strong>
        <strong class="text-primary">(-0.58%)</strong>
        <h6 class="mt-1 mx-1 mb-0">973.45원</h6>
        </div></div></div></li></a></ul></div></div><!--/ Transactions --></div>
    `

}

function search(e) {
    const val = e.target.value
    const filterData = data.filter((text) => {
        const regex = new RegExp(val, 'gi')
        return text.match(regex)
    })
    if (filterData) {
        let html = ""
        filterData.map((data) => {
            html += template(data.split(",")[1])
        })
        search_list.innerHTML = html
    }
}

window.onload = async function(){
    await getCountry()

    search_list = document.getElementById("search_list")
    const searchElement = document.getElementById("search")

    searchElement.addEventListener("keyup", search)



}

