/*
 * Bootstrap Cookie Alert by Wruczek
 * https://github.com/Wruczek/Bootstrap-Cookie-Alert
 * Released under MIT license
 */
(function () {
  "use strict";

  var cookieAlerta = document.querySelector(".cookie-alerta");
  var aceitarCookiesConheca = document.querySelector(".aceitar-cookies-conheca");
  var aceitarCookiesEntendi = document.querySelector(".aceitar-cookies-entendi");

  if (!cookieAlerta) {
    return;
  }

  cookieAlerta.offsetHeight; // (https://stackoverflow.com/a/39451131)

  // Se nao encontrar o cookie, apresenta o alerta
  if (!getCookie("politica_cookies_portal_informada")) {
    cookieAlerta.classList.add("show");
  }

  // Quando clicar no link, o cookie politica_cookies_portal_informada sera criado e tera validade por 7 dias e o alerta
  // sera fechado
  aceitarCookiesConheca.addEventListener("click", function () {
    setCookie("politica_cookies_portal_informada", true, 7);
    cookieAlerta.classList.remove("show");

    // Dispara um evento caso seja necessario trata-lo
    window.dispatchEvent(new Event("politicaCookiesPortalInformada"))
  });

  aceitarCookiesEntendi.addEventListener("click", function () {
    setCookie("politica_cookies_portal_informada", true, 7);
    cookieAlerta.classList.remove("show");

    // Dispara um evento caso seja necessario trata-lo
    window.dispatchEvent(new Event("politicaCookiesPortalInformada"))
  });

  // Funcoes para gerenciar o cookie do w3schools
  function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }

  function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) === ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) === 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }
})();
