$(document).ready(function(){
  var accessToken = localStorage.getItem("accessToken");
  if (!accessToken) {
    $('#loginModal').modal('show');
  }
});

function closeLoginModal() {
     $('#loginModal').modal('hide');
}
