$(document).ready(function(){
  $('#loginModal').modal('show');
});

function closeLoginModal() {
    const loginModal = document.getElementById('loginModal');
    loginModal.style.display = 'none';
}
