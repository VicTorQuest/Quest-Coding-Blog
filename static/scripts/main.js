const cookieContainer = document.querySelector('.cookie-container');
const cookieButton = document.querySelector('.cookie-btn');
const body = document.querySelector("body");
const navbar = document.querySelector(".navbar");
const menuBtn = document.querySelector(".menu-btn");
const cancelBtn = document.querySelector(".cancel-btn");
const btnScrollToTop = document.querySelector("#btnScrollToTop")
const search = document.querySelector('.search')


$(window).scroll(function() {
    if ($(this).scrollTop() > 300) {
      $('#btnScrollToTop').fadeIn();
    } else {
      $('#btnScrollToTop').fadeOut();
    }
  });

btnScrollToTop.addEventListener('click', function() {
    window.scrollTo(0, 0)
})




cookieButton.addEventListener("click", () => {
    cookieContainer.classList.remove("active");
    localStorage.setItem('cookieBannerDisplayed', 'true')
});

setTimeout( () => {
    if (!localStorage.getItem("cookieBannerDisplayed")) {
        cookieContainer.classList.add("active");
    }
}, 2000);


menuBtn.onclick = () => {
    navbar.classList.add("show");
    menuBtn.classList.add("hide");
    body.classList.add("disabled");
}
cancelBtn.onclick = () => {
    body.classList.remove("disabled");
    navbar.classList.remove("show");
    menuBtn.classList.remove("hide");
}
window.onscroll = () => {
    this.scrollY > 20 ? navbar.classList.add("sticky") : navbar.classList.remove("sticky");
    this.scrollY > 20 ? btnScrollToTop.classList.add("showbtnscrolltotop") : btnScrollToTop.classList.remove("showbtnscrolltotop");
}



$(document).ready(function(){

    $("#searchSm").click(function () {
        $(".search-box").toggle();
        $("input[type='search']").focus();
    });    
})