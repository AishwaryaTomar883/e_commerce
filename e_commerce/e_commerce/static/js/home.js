$(document).ready(function(){
  var accessToken = localStorage.getItem("accessToken");
  if (!accessToken) {
    $('#loginModal').modal('show');
  } else {
    var expirationTime = localStorage.getItem("accessTokenExpiration");
    if (expirationTime && new Date(expirationTime) < new Date()) {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("accessTokenExpiration");
      $('#loginModal').modal('show');
    }
  }
});

function closeLoginModal() {
     $('#loginModal').modal('hide');
}
