const names__field = [
    'input[name="name"]',
    'input[name="username"]',
    'input[name="email"]',
    'input[name="password1"]',
    'input[name="password2"]'
];

names__field.forEach(selector => {
    const el = document.querySelector(selector);
    if (el) {
        el.removeAttribute("required");
    }
});


const form = document.getElementById('signup_form');


form.addEventListener('submit', (e) => {
    e.preventDefault();

    const name = document.querySelector('input[name="name"]').value.trim();
    const username = document.querySelector('input[name="username"]').value.trim();
    const email = document.querySelector('input[name="email"]').value.trim();
    const password1 = document.querySelector('input[name="password1"]').value.trim();
    const password2 = document.querySelector('input[name="password2"]').value.trim();

    const nameError = document.querySelector('.error-name');
    const usernameError = document.querySelector('.error-username');
    const emailError = document.querySelector('.error-email');
    const password1Error = document.querySelector('.error-password1');
    const password2Error = document.querySelector('.error-password2');

    let status = true;

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!name) {
        nameError.innerText = "This field cannot be left empty";
        nameError.style.display = 'block';
        status = false;
    }

    if (!username) {
        usernameError.innerText = "This field cannot be left empty";
        usernameError.style.display = 'block';
        status = false;
    }

    if (!email || !emailRegex.test(email)) {
        emailError.style.display = 'block';
        emailError.innerHTML = "Please enter a valid email (e.g., user@example.com)."
        status = false;
    }

    if (!password1) {
        password1Error.innerText = "This field cannot be left empty";
        password1Error.style.display = 'block';
        status = false;
    }

    if (!password2) {
        password2Error.innerText = "This field cannot be left empty";
        password2Error.style.display = 'block';
        status = false;
    }

    if(password1 !== password2){
        password1Error.innerText = "Passwords didn't match";
        password1Error.style.display = 'block';
        status = false;
    }

    if (status) {
        e.target.submit();
    }

    return status == true;
});
