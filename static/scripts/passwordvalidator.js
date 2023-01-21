function _id(name) {
    return document.getElementById(name);
}

function _class(name) {
    return document.getElementsByClassName(name);
}

_class("toggle-password")[0].addEventListener("click", function() {
    _class("toggle-password")[0].classList.toggle("active");
    if(_id("password-field").getAttribute("type") ==  "password" ) {
        _id("password-field").setAttribute("type", "text");
    }
    else {
        _id("password-field").setAttribute("type", "password");
    }
});


_id("password-field").addEventListener('focus', function() {
    _class("password-policies")[0].classList.add("active");
});

_id("password-field").addEventListener('blur', function() {
    _class("password-policies")[0].classList.remove("active");
});



_class("toggle-login-password")[0].addEventListener("click", function() {
    _class("toggle-login-password")[0].classList.toggle("active");
    if(_id("login-password-field").getAttribute("type") ==  "password" ) {
        _id("login-password-field").setAttribute("type", "text");
    }
    else {
        _id("login-password-field").setAttribute("type", "password");
    }
});




_id("password-field").addEventListener('keyup', function() {
    let password  = _id("password-field").value;

    if (/[A-Z]/.test(password)) {
        _class("policy-uppercase")[0].classList.add("active");
        _class("pu-validate")[0].classList.add("validated");
    }
    else {
        _class("policy-uppercase")[0].classList.remove("active");
        _class("pu-validate")[0].classList.remove("validated");
    }


    if (/[0-9]/.test(password)) {
        _class("policy-number")[0].classList.add("active");
        _class("pn-validate")[0].classList.add("validated");
    }
    else {
        _class("policy-number")[0].classList.remove("active");
        _class("pn-validate")[0].classList.remove("validated");
    }


    if (/[^A-Za-z0-9]/.test(password)) {
        _class("policy-special")[0].classList.add("active");
        _class("ps-validate")[0].classList.add("validated");
    }
    else {
        _class("policy-special")[0].classList.remove("active");
        _class("ps-validate")[0].classList.remove("validated");
    }


    if (password.length > 7 && password.length < 15) {
        _class("policy-length")[0].classList.add("active");
        _class("pl-validate")[0].classList.add("validated");
    }
    else {
        _class("policy-length")[0].classList.remove("active");
        _class("pl-validate")[0].classList.remove("validated");
    }
})


const form = document.getElementById('registerform')
const password = document.getElementById("password-field")
const errorElement = document.getElementById("error")

form.addEventListener("submit", (e) => {
    let messages = []
    
    if (password.value.length < 8) {
        messages.push('password must be between 8-15 characters.')
    }

    if (password.value.length > 15) {
        messages.push('password must be between 8-15 characters.')
    }

    if (password.value.search(/[A-Z]/) < 0) {
        messages.push('password must contain an uppercase.')
    }

    if (password.value.search(/[0-9]/) < 0) {
        messages.push('password must contain a number.')
    }
  
    if (password.value.search(/[^A-Za-z0-9]/) < 0) {
        messages.push('password must contain a special character(! " ? $ % ^ & ).')
    }

    if (messages.length > 0) {
        e.preventDefault()
        errorElement.innerText = messages.join('\n ')
    }

})