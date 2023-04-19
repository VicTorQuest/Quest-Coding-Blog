$('#likePost').on('submit', function(e){
    e.preventDefault()
    $.ajax({
        type: 'GET',
        url: $(this).attr('action'),
        success: function(response) {
            if (response.liked) {
                $('.dislike-icon').empty()
                $('.dislike-count').empty()
                $('.dislike-verbal-name').empty()
                $('.like-icon').empty()
                $('.like-count').empty()
                $('.like-verbal-name').empty()
                dislikedtemp = "<i class='bi bi-hand-thumbs-down'></i>"
                likedtemp = "<i class='bi bi-hand-thumbs-up-fill'></i>"
                if (response.likes > 1) {
                    verbal_name = 'Likes'
                }else{
                    verbal_name = 'Like'
                }
                if (response.dislikes > 1) {
                    dislikeverbal_name = 'Dislikes'
                }else{
                    dislikeverbal_name = 'Dislike'
                }
                $('.dislike-icon').html(dislikedtemp)
                $('.dislike-count').html(response.dislikes+" "+dislikeverbal_name)
                $('.like-icon').html(likedtemp)
                $('.like-count').html(response.likes+" "+verbal_name)
            }else{
                $('.like-icon').empty()
                $('.like-count').empty()
                $('.like-verbal-name').empty()
                unlikedtemp = "<i class='bi bi-hand-thumbs-up'></i>"
                if (response.likes > 1) {
                    verbal_name = 'Likes'
                }else{
                    verbal_name = 'Like'
                }
                $('.like-icon').html(unlikedtemp)
                $('.like-count').html(response.likes+" "+verbal_name)
            }
        },
        error: function(error) {
        }
    })
})

$('#dislikePost').on('submit', function(e){
    e.preventDefault()
    $.ajax({
        type: 'GET',
        url: $(this).attr('action'),
        success: function(response) {
            if (response.disliked) {
                $('.like-icon').empty()
                $('.like-count').empty()
                $('.like-verbal-name').empty()
                $('.dislike-icon').empty()
                $('.dislike-count').empty()
                $('.dislike-verbal-name').empty()
                likedtemp = "<i class='bi bi-hand-thumbs-up'></i>"
                dislikedtemp = "<i class='bi bi-hand-thumbs-down-fill'></i>"
                if (response.dislikes > 1) {
                    dislikeverbal_name = 'Dislikes'
                }else{
                    dislikeverbal_name = 'Dislike'
                }
                if (response.likes > 1) {
                    likeverbal_name = 'Likes'
                }else{
                    likeverbal_name = 'Like'
                }
                $('.like-icon').html(likedtemp)
                $('.like-count').html(response.likes+" "+likeverbal_name)
                $('.dislike-icon').html(dislikedtemp)
                $('.dislike-count').html(response.dislikes+" "+dislikeverbal_name)
            }else{
                $('.dislike-icon').empty()
                $('.dislike-count').empty()
                $('.dislike-verbal-name').empty()
                undislikedtemp = "<i class='bi bi-hand-thumbs-down'></i>"
                if (response.dislikes > 1) {
                    verbal_name = 'Dislikes'
                }else{
                    verbal_name = 'Dislike'
                }
                $('.dislike-icon').html(undislikedtemp)
                $('.dislike-count').html(response.dislikes+" "+verbal_name)
            }
        },
        error: function(error) {
        }
    })
})