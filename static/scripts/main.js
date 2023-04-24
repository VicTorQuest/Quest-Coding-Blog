const cookieContainer = document.querySelector('.cookie-container');
const cookieButton = document.querySelector('.cookie-btn');
const body = document.querySelector("body");
const navbar = document.querySelector(".navbar");
const menuBtn = document.querySelector(".menu-btn");
const cancelBtn = document.querySelector(".cancel-btn");
const btnScrollToTop = document.querySelector("#btnScrollToTop")
const icon = document.querySelector('.search_icon')
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

icon.onclick = function() {
    search.classList.toggle('active')
}

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

    setInterval(function(){
        $.ajax({
            type: 'GET',
            url: '/getting_cart_total/',
            success: function(response){
          
                

                if (response.cartitems > 0) {
                    var cartTemplate = "<a href="+cartUrl+">"+"<img id='cart-icon' src='/static/store/images/cart.png'></a>"
                    var cartTemplate2 = "<p id='cart-total'>"+cartTotal+"</p>"
                    $('#cart-item-indicator:first').addClass('form-inline')
                    $('#cart-item-indicator').show()
                    $('#cart-total').empty();
                    var temp=response.cartitems
                    $('#cart-total').append(temp);
                }else {
                    $('#cart-item-indicator').hide()
                    // $('#cart-item-indicator').remove();
                }


            },
            error: function(response){
            }
        })
    }, 2000);

    
    
})