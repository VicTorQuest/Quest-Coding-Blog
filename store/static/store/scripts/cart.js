var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        var thisBtn = document.querySelectorAll(`[data-product="${productId}"]`);
        
        this.innerHTML = "Add to Cart<div class='loader-sm ml-2'><span class='loader-sm-inner'></span></div>" 
        this.style.pointerEvents = 'none'
        

        if (user == 'AnonymousUser') {
            addCookieItem(productId, action)
            this.innerHTML = "Add to Cart"
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
                }
            })
        }
    })
}


function addCookieItem(productId, action) {
    if (action == 'add') {
        if (cart['items'][productId] === undefined ) {
            cart['items'][productId] = {'quantity': 1}
        }else {
            cart['items'][productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart['items'][productId]['quantity'] -= 1

        if (cart['items'][productId]['quantity'] <= 0) {
            delete cart['items'][productId]
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    // location.reload()
}