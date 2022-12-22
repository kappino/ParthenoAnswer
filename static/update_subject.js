let showTime = 500;
let fadeOutTime = 44000;

$(document).ready(function () {
    // Making sure the elements are not visible even while loading the page using a temporary class hidden.
    let successText = $('#success')
    let failureText = $('#failure')
    successText.removeClass('hidden').hide();
    failureText.removeClass('hidden').hide();
    $('#post').submit(function (e) {
        e.preventDefault();
        $.ajax({
        type: 'POST',
        url: window.location.href,
        data: {
        new_subj: $("#new_subj").val()
    },
    success: (result) => {
        successText.hide();
        failureText.hide();
        let new_subj = $("#new_subj").val();
        if (result === "success") {
            let successString = `Successfully updated ${ new_subj } `;
            successText.text(successString).show(showTime).fadeOut(fadeOutTime);
        }
        else {
            let failString = `Failed to submit: ${ result }`;
            failureText.text(failString).show(showTime).fadeOut(fadeOutTime);
        }
    },
    error: function(error) {
        console.log("Error: " + JSON.stringify(error));
        }
    })
    });
});