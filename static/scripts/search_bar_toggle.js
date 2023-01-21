const icon = document.querySelector('.search_icon')
const search = document.querySelector('.search')
icon.onclick = function() {
    search.classList.toggle('active')
}