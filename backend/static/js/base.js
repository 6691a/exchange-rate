window.onpageshow = function (event) {
    if ( event.persisted || (window.performance && window.performance.navigation.type == 2)) {
        //뒤로가기 후 새로고침
        location.reload(true);
    }
    // else {
    //
    // }
}