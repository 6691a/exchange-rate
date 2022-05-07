
let socket
const protocol = (window.location.protocol === 'https:' ? 'wss' : 'ws') + '://'
const path = protocol + window.location.host + '/ws/exchange_rate/'
function socket_connect(name) {
    if (!socket) {
        socket = new WebSocket(
            path + name + '/'
        )
    }
    else if (socket.url.indexOf(name) === -1) {
        socket.close()
        socket = new WebSocket(
            path + name + '/'
        )
    }
    add_socket_event()

}
function add_socket_event() {
    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data)
    };
}

document.querySelector('#socket_1').onclick = function (e) {
    socket_connect(this.value)
}
document.querySelector('#socket_2').onclick = function (e) {
    socket_connect(this.value)
}
