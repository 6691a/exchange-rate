const data = []

async function getCountry() {
    const res = await http.get("exchange_rate/country/")

    if (res.status !== 200) {
        // 실패 안내 출력
    }
    console.log(res.data)
}
