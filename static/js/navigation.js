// search-box open close js code
let navbar = document.querySelector(".navbar");
let searchBox = document.querySelector(".search-box .fa-search");

$(()=>{
    $(window).on("scroll", ()=>{
     if ($(window).scrollTop() > 150) {
      $('.snav').addClass('fixed');
    } else {
      $('.snav').removeClass('fixed');
     }
    })
  })

searchBox.addEventListener("click", ()=>{
  navbar.classList.toggle("showInput");
  if(navbar.classList.contains("showInput")){
    searchBox.classList.replace("fa-search" ,"fa-times");
  }else {
    searchBox.classList.replace("fa-times" ,"fa-search");
  }
});

// sidebar open close js code
let navLinks = document.querySelector(".nav-links");
let menuOpenBtn = document.querySelector(".navbar .bx-menu");
let menuCloseBtn = document.querySelector(".nav-links .bx-x");
menuOpenBtn.onclick = function() {
navLinks.style.left = "0";
}
menuCloseBtn.onclick = function() {
navLinks.style.left = "-100%";
}

// sidebar submenu open close js code
let skincareArrow = document.querySelector(".skincare-arrow");
skincareArrow.onclick = function() {
 navLinks.classList.toggle("show1");
}
let faceArrow = document.querySelector(".face-arrow");
faceArrow.onclick = function() {
 navLinks.classList.toggle("show2");
}
let bodyArrow = document.querySelector(".body-arrow");
bodyArrow.onclick = function() {
 navLinks.classList.toggle("show3");
}
let lipsEyesArrow = document.querySelector(".lips-eyes-arrow");
lipsEyesArrow.onclick = function() {
 navLinks.classList.toggle("show4");
}
let hairArrow = document.querySelector(".hair-arrow");
hairArrow.onclick = function() {
 navLinks.classList.toggle("show5");
}
let profileArrow = document.querySelector(".profile-arrow");
profileArrow.onclick = function() {
 navLinks.classList.toggle("show8");
}
