const names__field = [
    'input[name="name"]',
    'input[name="topic"]',
    'input[name="description"]'
];

names__field.forEach(selector => {
    const el = document.querySelector(selector);
    if (el) {
        el.removeAttribute("required");
    }
});

form = document.querySelector('#create_room_form');

form.addEventListener("submit", (e) => {
    e.preventDefault();

    let status = true;

    room_topic_input = document.querySelector('input[name="topic"]').value.trim();
    room_name_input = document.querySelector('input[name="name"]').value.trim();
    room_description_input = document.querySelector('textarea[name="description"]').value.trim();

    room_topic_error = document.querySelector('.room_topic_error');
    room_name_error = document.querySelector('.room_name_error');
    room_description_error = document.querySelector('.room_description_error');

    if(!room_topic_input){
        status = false;
        room_topic_error.style.display = "block";
        room_topic_error.innerHTML = "This field need to be filled";
    }

    if(!room_name_input){
        status = false;
        room_name_error.style.display = "block";
        room_name_error.innerHTML = "This field need to be filled";
    }

    if(!room_description_input){
        status = false;
        room_description_error.style.display = "block";
        room_description_error.innerHTML = "This field need to be filled";
    }

    if(status){
        e.target.submit();
    }

    return status == true;
});
