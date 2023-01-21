$(document).ready(function() {
    setInterval(function(){
        $.ajax({
            type: "GET",
            url: "/getting_item_number/",
            data: {'product_id': product_id},
            success: function(response) {
                $("#product-quantity").val(response.quantity)                
            }
        })
    }, 1000)
})