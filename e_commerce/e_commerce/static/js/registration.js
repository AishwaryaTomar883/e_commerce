function performRegister() {
    const form = document.getElementById('registerForm');
    const formData = new FormData(form);

    $.ajax({
        url: '/user/api/v1/register_api/',
        type: 'post',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response, textStatus, jqXHR) {
            var msg = "";
            if(jqXHR.status === 200){
                redirectToLogin();
            } else {
                msg = response.error;
                alert(msg);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            // Check if the server provided an error message
            if (jqXHR.responseJSON) {
                if (jqXHR.responseJSON.email) {
                    alert(jqXHR.responseJSON.email[0]);
                } else if (jqXHR.responseJSON.password) {
                    alert(jqXHR.responseJSON.password[0]);
                } else {
                    alert("An error occurred during registration.");
                }
            } else {
                alert("An error occurred during registration.");
            }
        }
    });
}
