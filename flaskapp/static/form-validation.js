$(document).ready(function(){
    $('#contact').validate({
        rules: {
            name: {
                required: true,
                minlength: 2
            },
            surname: {
                required: true,
                minlength: 2
            },
            email: {
                required: true,
                email: true
            },
            subject: {
                required: true
            },
            text: {
                required: true
            }
        }
    });

    $('#add-entry').validate({
        rules: {
            title: {
                required: true
            },
            text: {
                required: true
            }
        }
    });
})