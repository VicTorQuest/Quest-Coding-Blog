var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('User:', user)
        if (user == 'AnonymousUser') {
            addCookieItem(productId, action)
        }
        else {
            $.ajax({
                type: 'POST',
                url: '/update-item/',
                data:  {'productId': productId, 'action': action},
                csrfmiddlewaretoken: csrftoken,
                success: function(data){
                    console.log(data)
                    
                }
            })
        }
    })
}



// $('#displayCartItems').ready(function() {
//     var updateBtns = document.getElementsByClassName('update-cart')
//     updateBtns.addEventListener('click', function(){
//         var productId = this.dataset.product
//         var action = this.dataset.action
//         console.log('productId:', productId, 'action:', action)

//         console.log('User:', user)
//         if (user == 'AnonymousUser') {
//             addCookieItem(productId, action)
//         }
//         else {
//             $.ajax({
//                 type: 'POST',
//                 url: '/update-item/',
//                 data:  {'productId': productId, 'action': action},
//                 csrfmiddlewaretoken: csrftoken,
//                 success: function(data){
//                     console.log(data)
                    
//                 }
//             })
//         }
//     })
//   });

// $(document).on('click', '#update-cart', function() {
//     console.log('add to cart clicked')
//     var productId = this.dataset.product
//     var action = this.dataset.action
//     console.log('productId:', productId, 'action:', action)
    
//     console.log('User:', user)
//     console.log(csrftoken)
//     if (user == 'AnonymousUser') {
//         addCookieItem(productId, action)
//     }
    
//     else {
//         $.ajax({
//             type: 'POST',
//             url: '/update-item/',
//             data:  {'productId': productId, 'action': action},
//             csrfmiddlewaretoken: csrftoken,
//             success: function(data){
//                 console.log(data)
                
//             }
//         })
//     }
// })




function addCookieItem(productId, action) {
    console.log('user is not authenticated....')

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
            console.log('item deleted')
        }
    }
    console.log(cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    // location.reload()
}

// function updateUserOrder(productId, action) {
//     console.log('user is logged in sending data....')

//     var url = '/update-item/'

//     fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrftoken,         
//         },
//         body:JSON.stringify({'productId': productId, 'action': action})
//     })

//     .then((response) =>{
//         return response.json()
//     })

//     .then((data) =>{
//         console.log('data:', data)
//         location.reload()
//     })
// }