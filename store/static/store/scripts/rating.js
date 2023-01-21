    const one = document.getElementById('first')
    const two = document.getElementById('second')
    const three = document.getElementById('third')
    const four = document.getElementById('fourth')
    const five = document.getElementById('fifth')
  
    const ratings = document.querySelector(".rating-stars")
    const form = document.getElementById("rate-form")
    const confirmBox = document.getElementById("confirm-box")
    const errordiv = document.getElementById("error-div")
    const rating = document.getElementById('rating')
    const submitBtn = document.getElementById('submit-review')
    const csrf = document.getElementsByName("csrfmiddlewaretoken")
    const handlerstarselect = (size)=> {
        const children = ratings.children
        for (let i=0; i < children.length; i++) {
            if(i < size) {
                children[i].classList.add('checked')
            }else {
                children[i].classList.remove('checked')
            }
        }
    }


  
    const handleselect = function(selection) {
      switch (selection) {
        case 'first':
          {
            // one.classList.add('checked')
            // two.classList.remove('checked')
            // three.classList.remove('checked')
            // four.classList.remove('checked')
            // five.classList.remove('checked')
            handlerstarselect(1)
            return
          }
        case 'second':
          {
            handlerstarselect(2)
            return
          }
  
        case 'third':
          {
            handlerstarselect(3)
            return
          }
  
        case 'fourth':
          {
            handlerstarselect(4)
            return
          }
  
        case 'fifth':
          {
            handlerstarselect(5)
            return
          }
      }
    }


    const getNumericValue = (strngValue) => {
      let numericValue
      if (strngValue === 'first') {
        numericValue = 1
      } 

      else if(strngValue == 'second') {
        numericValue = 2
      }

      else if(strngValue == 'third') {
        numericValue = 3
      }

      else if(strngValue == 'fourth') {
        numericValue = 4
      }

      else if(strngValue == 'fifth') {
        numericValue = 5
      }
      else {
        numericValue = 0
      }
      return numericValue
    }


    const genrateStarRating = function(rating) {
      let ratingString
      console.log(rating)
      if (rating == 1) {
        ratingString = `<i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star'></i><i class='bi bi-star-fill star'></i><i class='bi bi-star-fill star'></i><i class='bi bi-star-fill star'></i>`
      }

      else if (rating == 2) {
        ratingString = `<i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star'></i><i class='bi bi-star-fill star'></i><i class='bi bi-star-fill star'></i>`
      }

      else if(rating == 3) {
        ratingString = `<i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star'></i><i class='bi bi-star-fill star'></i>`
      }

      else if(rating == 4) {
        ratingString = `<i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star'></i>`
      }

      else if (rating == 5) {
        ratingString = `<i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star checked'></i><i class='bi bi-star-fill star checked'></i>`
      }

      else {
        ratingString = `<i class='bi bi-star-fill star '></i><i class='bi bi-star-fill star '></i><i class='bi bi-star-fill star '></i><i class='bi bi-star-fill star '></i><i class='bi bi-star-fill star '></i>`
      }
      return ratingString
    }

    const arr = [one, two, three, four, five]
    const sleep = (milliseconds) => {
      return new Promise(resolve => setTimeout(resolve, milliseconds))
    }
  
    arr.forEach(item => item.addEventListener('mouseover', (event) => {
      handleselect(event.target.id)   
    }))
    
    arr.forEach(item => item.addEventListener('click', (event)=>{     
      const val = event.target.id
      let isRated = false
      rating.value = getNumericValue(val)
      if (isRated) {
        return
      }
      isRated = true
    }))

    form.addEventListener('submit', e=>{
      e.preventDefault()
      
      if (rating.value == "") {
        errordiv.innerHTML = "<small class='text-danger d-block pb-2'><i class='bi bi-exclamation-triangle'></i> Please select your rating</small>"
        return
      }
      const review = document.getElementById("review")
      if (review.value == "") {
        errordiv.innerHTML = "<small class='text-danger d-block pb-2'><i class='bi bi-exclamation-lg'></i> Please fill in your review</small>"
        return
      }
      errordiv.innerHTML = ""
      submitBtn.innerHTML = "Submitting &nbsp; <div class='spinner-border spinner-border-sm' role='status'><span class='visually-hidden'>Loading...</span></div>"
      submitBtn.style.pointerEvents = 'none'
      
      
      $(".spinner-border").fadeIn('slow')
      $.ajax({
        type: 'POST',
        url: '/rate/',
        data: {'csrfmiddlewaretoken': csrf[0].value, 'rating': rating.value, 'review': review.value, 'product_id': product_id},
        success: function(response){
          $(".spinner-border").fadeOut('slow')
          submitBtn.innerHTML = "Done"
          $("#review-form-header").fadeOut('slow')
          $("#rate-form").fadeOut('slow')
          confirmBox.innerHTML =  "<div class='alert alert-success' role='alert'>Your review was submitted, Thanks for the feedback.</div>"
          var newReview = `<div class='mb-4'><div class='d-flex justify-content-between'><div class='d-flex customer align-items-center'><div class='review-image-area'><img src='${response.image}' alt='customer image'></div><div class='text-white name ms-3'><p>${response.email}</p><i>${response.date}</i></div></div><div class='ratings'>${genrateStarRating(response.rating)}</div></div><div class='pt-2 text-white review-comment'><p>${response.review}.</p></div></div>`
          $(".review").prepend(newReview)
        },
        error: function(){
          
          
         
  
          async function timeSensativeAction(){ 
            confirmBox.innerHTML =  `<div class='alert alert-danger' role='alert'>Can't rate this product right now</div>`
            await sleep(5000)
            $(".alert").fadeOut("slow")
          }
          
        }
      })
    })