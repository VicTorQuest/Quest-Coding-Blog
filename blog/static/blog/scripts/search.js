$(document).ready(function() {
    $('#searchForm').submit(function(e) {
        e.preventDefault()
        query = $('#seacrhtextbox').val()
        $('#blogContent').html(`<div class="text-white mb-5 d-flex align-items-center justify-content-center">Searching <div class="loader-sm ml-2"><span class="loader-sm-inner"></span></div></div>`)
        
        let loopdata;
        function loopCategory(array, arrayurl) {
            loopdata = ``
            for (let i = 0; i < array.length; i++) {
                loopdata+=`<a href="${arrayurl[i]}" class="btn tag mr-2">${array[i]}</a>`;
               }
             return loopdata;
        }
        $.ajax({
            type: 'GET',
            url: '/search-query/',
            data: {'query': query},
            success: function(response) {
                if (Array.isArray(response.posts)) {
                    $('#blogContent').empty()
                    if (response.posts.length > 0) {
                        response.posts.forEach(post => {
                            $('#blogContent').append(`
                                <div class="col-md-12 mb-5 pb-2 post">
                                    <div class="tag-area">
                                    ${loopCategory(post.category, post.category_url)}
                                    </div>
                                
                                    <div class="post-img-area p-lg-2 pt-3 pt-lg-4 pb-0">
                                        <img src="${post.post_img}" loading='lazy' class="post-img" alt="post image">
                                    </div>
                                    <h2 class="mt-4 text-center mx-4"><a class="post-h2-link" href="${post.post_url}">${post.title}</a></h2>
                                    
                                    <div class="post-icons text-center my-3 mt-lg-4 mx-lg-4 mx-sm-2">
                                        <a href="${post.author_url}" class="owner"><img class="owner-img mr-2" alt="author image" loading='lazy' src="${post.author_img}" alt="">${post.author}</a>
                                        <span class="date"><i class="bi bi-calendar ml-2 mr-2"></i>${post.date}</span>
                                        <a class="comment-link ml-4 mr-2" href="${post.post_url}#comments"><i class="bi bi-chat-dots mr-2"></i>${post.total_comments}</a>
                                        <i class="bi bi-eye ml-3 mx-2"></i>${post.hitcount}
                                    </div>
                                    
                             
                                    <p class="text-center mx-lg-5 mx-2 post-detail">${post.intro.slice(0, 175)}....</p>
                                    <div class="text-center mt-4">
                                        <a href="${post.post_url}" class="btn continue-reading text-center mb-4">Continue reading</a>
                                    </div>
                                </div>`)
                            });
                            $('#seachResultHeader').text(`Search results for: "${query}"`)
                            word = query
                            myHilitor = new Hilitor("blogContent"); // id of the element to parse
                            myHilitor.apply(word);
                    } else {
                        $('#seachResultHeader').text(`Search results for: "${query}"`)
                        $('#blogContent').html(`<h2 class='text-white col-md-12 mb-5' id='noResultHeader'>No result for the given query: '${response.query}'.....<i class='bi bi-emoji-dizzy'></i></h2>`) 
                    }
                }else {
                    if ($('#seacrhtextbox').val().length > 0) {
                        $('#seachResultHeader').text(`Search results for: "${query}"`)
                        $('#blogContent').html(`<h2 class='text-white col-md-12 mb-5' id='noResultHeader'>No result for the given query: '${response.query}'.....<i class='bi bi-emoji-dizzy'></i></h2>`)
                    } 
                }                
            },
            error: function(error) {
                $('#seachResultHeader').text(`Search results for: "${query}"`)
                $('#blogContent').html(`<h2 class='text-white col-md-12 mb-5 mt-4'>No result for the given query: '${response.query}'.....<i class='bi bi-emoji-dizzy'></i></h2>`)
            }
        })
    })
})