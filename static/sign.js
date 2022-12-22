let error = $('#error');
error.removeClass('hidden').hide();

$(document).ready(function () {
    $('#sign_in').submit(sign);
});

$(document).ready(function () {
    $('#sign_up').submit(sign);
});

function sign(e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: window.location.href,
        data: {
        username: $("#username").val(),
        password: $("#password").val(),
    },
    success: (result) => {
            window.location = '/profile';
    },
    error: (result) => {
         error.text(result.responseJSON).show().fadeOut(3000, 'swing');
        }
    });
}