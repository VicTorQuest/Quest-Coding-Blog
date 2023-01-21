const cookieContainer = document.querySelector('.cookie-container');
const cookieButton = document.querySelector('.cookie-btn');


cookieButton.addEventListener("click", () => {
    cookieContainer.classList.remove("active");
    localStorage.setItem('cookieBannerDisplayed', 'true')
});

setTimeout( () => {
    if (!localStorage.getItem("cookieBannerDisplayed")) {
        cookieContainer.classList.add("active");
    }
}, 2000);

$(document).ready(function(){

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
                    // if ($('#cart-item-indicator').length) {
                    //     $('#cart-item-indicator').empty();
                    //     $('#cart-item-indicator').append(cartTemplate, cartTemplate2);
                    // }
                    // else {
                    //     console.log('adding cart item indicator')
                    //     $('#cart-item-indicator').html(cartTemplate, cartTemplate2);
                    //     console.log('cart item indicator added')
                    // }                    
                    $('#cart-total').empty();
                    var temp=response.cartitems
                    $('#cart-total').append(temp);
                }else {
                    $('#cart-item-indicator').hide()
                    // $('#cart-item-indicator').remove();
                }


            },
            error: function(response){
                alert('error getting data')
            }
        })
    }, 2000);

    
    
})