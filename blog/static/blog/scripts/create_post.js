const csrf = document.getElementsByName('csrfmiddlewaretoken')

const csrf_token = (csrf[0].value)
const url = ""

$(document).ready(function() {
    $('#div_id_post_img').append(`<div id="img-box"></div>`)



    $('#id_post_img').change(function() {
        const img_data = this.files[0]
        const url = URL.createObjectURL(img_data)
        $('#img-box').html(`<img class='mt-2' src='${url}' width='220px' height='150px' />`)
    })

    $('#postForm').submit(function(e) {
        e.preventDefault()
        const fd = new FormData(this)
        fd.set('content', CKEDITOR.instances['id_content'].getData())
        // fd.set('category', $('#id_category').val())
        if ($('#id_post_img').prop('files')[0] != null) {
            $('.progress').removeClass('hide-progress')
            $('#progressPercentage').removeClass('hide-progress')
            $('.btn-post').html(`Uploading  <div class="loader-sm ml-1"><span class="loader-sm-inner"></span></div>`)
            $('.btn-post').css('pointer-events', 'none')
        }

        $.ajax({
            type: 'POST',
            url: '/create-post-api/',
            data: fd,
            processData: false,
            contentType: false, 
            beforeSend: function() {
                $('#newPost').empty()
            },
            xhr: function() {
                const xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', function(e) {
                    if (e.lengthComputable) {
                        const progressPercentage = (e.loaded / e.total) * 100                        
                        $('.progress').html(`<div class='progress-bar progress-bar-striped progress-bar-animated' role='progressbar' style='width: ${progressPercentage}%' aria-valuenow='${progressPercentage}' aria-valuemin='0' aria-valuemax='100'></div>`)
                        $('#progressPercentage').text(`${progressPercentage.toFixed(1)}%`)
                        
                    }
                })
                return xhr
            },
            success: function(response) {
                setTimeout(function() {
                    $('#postForm').trigger("reset")
                    CKEDITOR.instances['id_content'].setData('')
                    $('#img-box').empty()
                    $('.progress').html(`<div class='progress-bar bg-success' role='progressbar' style='width: 100%' aria-valuenow='100' aria-valuemin='0' aria-valuemax='100'></div>`)
                    $('#progressPercentage').text('100%')
                    $('.btn-post').empty()
                    $('.btn-post').text('Post')
                    $('.btn-post').css('pointer-events', '')
                    $('#newPost').html(`<h5 class='pt-4'>View Post: <a style='color:cyan' href='${response.post_url}'>${response.post_url}</a></h5>`)
                }, 2000)
            },
            error: function (jqXhr, textStatus, errorThrown) {
                $('#progressPercentage').text('')
                $('.btn-post').text('Post')
                $('.btn-post').css('pointer-events', '') 
                $('.progress-bar').addClass('bg-danger')
                $('.progress-bar').removeClass('progress-bar-striped')
                $('.progress-bar').removeClass('progress-bar-animated')
                $('#newPost').html(`<div class='alert alert-danger' role='alert'>Oops, something went wrong: ${jqXhr.responseText}</div>`)
            },
        })


    })
})