// JavaScript to toggle off-canvas menu
function menutoggle() {
    var offcanvas = document.getElementById('offcanvas');
    if (offcanvas.classList.contains('show')) {
        setTimeout(function () { offcanvas.classList.remove('show'); }, 500);
        // Delay removal to match transition time
    } else {
        offcanvas.classList.add('show');
    }
}
console.log('base script')
