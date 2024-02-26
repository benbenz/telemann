function modalOpen(disable=true) {
    document.getElementById('default-modal').classList.remove('hidden')
    if(disable)
        document.getElementById('mainsection').classList.add('disabled')
}
function modalClose() {
    document.getElementById('default-modal').classList.add('hidden')
    document.getElementById('mainsection').classList.remove('disabled')
}
document.addEventListener("DOMContentLoaded", (event) => {
    document.getElementById('modal-close').addEventListener('click',modalClose)
})