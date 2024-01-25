allowedSuccessStatusCodes = [200, 201]

function showSuccessMessage(msg) {
    toastr.success(msg)
}

function showErrorMessage(msg) {
    toastr.error(msg)
}

function showMessages(isSuccess, messages) {
    for (message of messages) {
        isSuccess ? showSuccessMessage(message) : showErrorMessage(message);
    }
}

function redirectAnotherPage(url) {
    if (url) {
        setTimeout(function () {
            window.location.href = url;
        }, 1000)
    }
}

function getTokens() {
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');
    return { accessToken, refreshToken };
}

function redirectToLogin() {
    window.location.href = '/user/api/v1/login/';
}

function refreshAccessToken(refreshToken) {
    $.ajax({
        url: '/user/api/v1/refresh-token/',
        type: 'post',
        data: { refresh_token: refreshToken },
        success: function(response) {
            localStorage.setItem('accessToken', response.access);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            redirectToLogin();
        }
    });
}

function ajaxCall(type, url, data, callBack, callBackFailed, contentType, processData) {
    $.ajax({
       url: url,
       type: type,
       data: data,
       contentType: contentType,
       processData: processData,
       beforeSend: function (xhr) {
        const accessToken = localStorage.getItem('accessToken');
        if (accessToken) {
            xhr.setRequestHeader('Authorization', 'Bearer ' + accessToken);
        } else {
            redirectToLogin();
        }
       },
       dataType: "json",

       success: function (response) {
        if (response && response.messages) {
            showMessages(allowedSuccessStatusCodes.includes(response.status_code), response.messages);
        }
        if (response && response.redirect_url) {
            redirectAnotherPage(response.redirect_url);
        }
        if (callBack) {
            callBack(response);
        }
       },

       error: function (jqXHR, textStatus, errorThrown) {
        if (jqXHR.status === 401) {
            refreshAccessToken(getTokens().refreshToken);
        } else {
            if (callBackFailed) {
                callBackFailed(jqXHR, textStatus, errorThrown);
            }
        }
       }
    });
}

function getRequest(url, data = {}, callBack = null, callBackFailed = null) {
    ajaxCall("GET", url, data, callBack, callBackFailed);
}

function postRequest(url, data = {}, callBack = null, callBackFailed = null, contentType="application/x-www-form-urlencoded; charset=UTF-8", processData=true) {
    ajaxCall("POST", url, data, callBack, callBackFailed, contentType, processData);
}

function patchRequest(url, data = {}, callBack = null, callBackFailed = null, contentType="application/x-www-form-urlencoded; charset=UTF-8", processData=true) {
    ajaxCall("PATCH", url, data, callBack, callBackFailed, contentType, processData);
}

function deleteRequest(url, data = {}, callBack = null, callBackFailed = null) {
    ajaxCall("DELETE", url, data, callBack, callBackFailed);
}
