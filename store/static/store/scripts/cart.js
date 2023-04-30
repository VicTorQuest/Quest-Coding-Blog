var updateBtns = document.getElementsByClassName('update-cart')


for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        var thisBtn = document.querySelectorAll(`[data-product="${productId}"]`);
        
        this.innerHTML = "Add to Cart<div class='loader-sm ml-2'><span class='loader-sm-inner'></span></div>" 
        this.style.pointerEvents = 'none'
        

        if (user == 'AnonymousUser') {
            addCookieItem(productId, action, this)
        }
        else {
            $.ajax({
                type: 'POST',
                url: '/update-item/',
                data:  {'productId': productId, 'action': action},
                csrfmiddlewaretoken: csrftoken,
                success: function(data){
                    thisBtn[0].innerHTML = "Add to Cart"
                    thisBtn[0].style.pointerEvents = ""
                    if ($("#product-quantity").length) {
                        $("#product-quantity").val(data.quantity) 
                    }

                    if (data.cartitems > 0) {
                        var cartTemplate = "<a href="+cartUrl+">"+"<img id='cart-icon' src='/static/store/images/cart.png'></a>"
                        var cartTemplate2 = "<p id='cart-total'>"+cartTotal+"</p>"
                        $('#cart-item-indicator:first').addClass('form-inline')
                        $('#cart-item-indicator').show()
                        $('#cart-total').empty();
                        var temp=data.cartitems
                        $('#cart-total').append(temp);
                    }else {
                        $('#cart-item-indicator').hide()
                        // $('#cart-item-indicator').remove();
                    }
                }
            })
        }
    })
}


function addCookieItem(productId, action, btn) {
    prodQuantity = document.getElementById('product-quantity')
    if (action == 'add') {
        if (cart['items'][productId] === undefined ) {
            cart['items'][productId] = {'quantity': 1}
        }else {
            cart['items'][productId]['quantity'] += 1
        }
        if (typeof(prodQuantity) != 'undefined' && prodQuantity != null) {
            console.log('yes')
            prodQuantity.value = cart['items'][productId]['quantity']
        }
    }

    if (action == 'remove') {
        cart['items'][productId]['quantity'] -= 1

        if (cart['items'][productId]['quantity'] <= 0) {
            delete cart['items'][productId]
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    btn.innerHTML = "Add to Cart"
    btn.style.pointerEvents = ''
    cartIndicator = document.getElementById("cart-item-indicator")
    cartTotal = document.getElementById('cart-total')
    var totalitems = 0
    for([key, val] of Object.entries(cart['items'])) {
        totalitems += val['quantity']
      }
        
    if (totalitems > 0) {
        var cartTemplate = "<a href="+cartUrl+">"+"<img id='cart-icon' src='/static/store/images/cart.png'></a>"
        var cartTemplate2 = "<p id='cart-total'>"+cartTotal+"</p>"
        cartIndicator.classList = "form-inline cart-item-indicator"
        cartIndicator.style.display = 'flex'
        cartTotal.innerHTML = ""
        cartTotal.innerHTML = totalitems 
    }else {
        $('#cart-item-indicator').hide()
        // $('#cart-item-indicator').remove();
    }
}