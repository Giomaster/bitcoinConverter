window.onbeforeunload = function () {
  if (localStorage.getItem('token')) { window.scrollTo(999999999999, 99999999999999999); }
  else { window.scrollTo(0, 0); }
}

window.onresize = function(event) {
  if (localStorage.getItem('token')) { window.scrollTo(999999999999, 99999999999999999); }
}

if (localStorage.getItem('token')) { getMoney(); }

function confCurrency() {
  $('#cardF').css({'transform': 'rotateX(180deg)'});
  $('#cardB').css({'transform': 'rotateX(360deg)'});
}

function backCurrency() {
  $('#cardF').css({'transform': 'rotateX(0deg)'});
  $('#cardB').css({'transform': 'rotateX(180deg)'});
}

function deslogar() {
  $.ajax({
    type: "GET",
    url: 'deslogar',
    success: function() {
      localStorage.clear();
      $('#content').animate({'margin-top': '0'}, 1500);
    }
  });
}

function getMoney() {
  $.ajax({
    type: "GET",
    url: '/api/btc',
    headers: { "Authorization": localStorage.getItem('token') },
    success: function(response) {
      const rj = JSON.parse(response);
      const currencies = document.getElementsByClassName('convertShow');
      const btc = document.getElementById('inBit').value;
      currencies[0].innerText = rj["bpi"]["USD"]["rate_float"] * btc;
      currencies[1].innerText = rj["bpi"]["BRL"]["rate_float"] * btc;
      currencies[2].innerText = rj["bpi"]["EUR"]["rate_float"] * btc;
      currencies[3].innerText = rj["bpi"]["CAD"]["rate_float"] * btc;
    },
    error: function(e) {
      message = JSON.parse(e["responseText"])
      console.log(message['message']);
    }
  });
}

function getCurrency() {
  const getSel = document.getElementById("targetCurrency");
  const value = document.getElementById("vaa");
  $.getJSON("static/btc/js/currencies.json?" + new Date().getTime(), function(json) {
    switch (getSel.value) {
      case "BRL":
        value.innerText = json["BRL"];
        break;
      case "EUR":
        value.innerText = json["EUR"];
        break;
      case "CAD":
        value.innerText = json["CAD"];
        break;
    }
  });
}

function updateCurrency() {
  const getSel = document.getElementById("targetCurrency");
  const val = document.getElementById("cva");
  console.log(val.value);
  // return false;

  $.ajax({
    type: "POST",
    url: '/api/btc',
    data: { "value": val.value, "currency": getSel.value },
    success: function(response) {
      const rj = JSON.parse(response);
      alert(rj["message"])
      getCurrency();
      backCurrency();
      getMoney();
    },
    error: function(e) {
      message = JSON.parse(e["responseText"])
      alert(message['message']);
    }
  });
}

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
      localStorage.setItem('token', rj["token"])
      $('#content').animate({'margin-top': '-100vh'}, 1500);
      getMoney();
    },
    error: function(e) {
      message = JSON.parse(e["responseText"])
      alert(message['message']);
    }
  });
}
