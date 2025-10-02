const form = document.getElementById('login_form');


form.addEventListener('submit', (e) => {
    e.preventDefault();

    const email = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const emailError = document.querySelector('.email-error');
    const passwordError = document.querySelector('.password-error');

    emailError.style.display = 'none';
    passwordError.style.display = 'none';

    let status = true;

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!email || !emailRegex.test(email)) {
        emailError.style.display = 'block';
        emailError.innerHTML = "Please enter a valid email (e.g., user@example.com)."
        status = false;
    }

    if (!password) {
        passwordError.innerText = "This field cannot be left empty";
        passwordError.style.display = 'block';
        status = false;
    }

    if(status){
        e.target.submit();
    }

    return status == true;
});
