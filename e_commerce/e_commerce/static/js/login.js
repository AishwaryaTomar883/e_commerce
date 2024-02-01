function performLogin() {
    const form = document.getElementById('loginForm');
    const formData = new FormData(form);

    $.ajax({
        url: '/user/api/v1/login_api/',
        type: 'post',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response, textStatus, jqXHR) {
            var msg = "";
            if(jqXHR.status === 200){
                localStorage.setItem('refreshToken', response.refresh);
                localStorage.setItem('accessToken', response.access);
                localStorage.setItem('accessTokenExpiration', response.expiration_time);
                window.location.href = '/user/api/v1/home/';
            } else {
                msg = response.error;
                alert(msg);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            // Check if the server provided an error message
            if (jqXHR.responseJSON && jqXHR.responseJSON.non_field_errors) {
                alert(jqXHR.responseJSON.non_field_errors[0]);
            } else {
                alert("An error occurred during login.");
            }
        }
    });
}
