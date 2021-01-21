function loginProcess() {
  const email = document.getElementById('email');
  const senha = document.getElementById('pass');
  const content = document.getElementById('content');

  $.ajax({
    type: "POST",
    url: '/api/login',
    data: { "email": email.value, "password": senha.value },
    success: function(response) {
      const rj = JSON.parse(response)
      if(rj["token"]) { $('#content').animate({'margin-top': '-100vh'}, 1500); }
      else { alert(rj['message']) }
    },
  });
}
