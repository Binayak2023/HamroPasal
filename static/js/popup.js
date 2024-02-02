// Popup
const popup = document.querySelector(".popup");
const closePopup = document.querySelector(".popup-close");

function setCookie(cname, cvalue, exmins) {
    const d = new Date();
    // d.setTime(d.getTime() + (exdays*24*60*60*1000));
    d.setTime(d.getTime() + exmins*60*1000);
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }

  // Get Cookie Function
  function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(";");
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == " ") {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

  // Check Cookie On Window On Load
  window.onload = function (event) {
    document.cookie = "showpopup=";
    if (getCookie("timetoshowpopup") == "no") {
      document.cookie = "showpopup=";
    } else if (getCookie("timetoshowpopup") == "") {
      setTimeout(function () {
        document.cookie = "showpopup=yes";
      }, 5000);
    }
  };

  // Whether to show popup or not
  document.onmousemove = function (event) {
    if (getCookie("showpopup") == "yes") {
      if (event.pageY <= 1) {
        if (popup) {
            popup.classList.remove("hide-popup");

            closePopup.addEventListener("click", () => {
              popup.classList.add("hide-popup");
            });
          }
        setCookie("timetoshowpopup", "no", 10);
        document.cookie = "showpopup=";
      }
    }
  };