// Hero Carousel
const slider1 = document.querySelector("#glide_1");
if (slider1) {
  new Glide(slider1, {
    type: "carousel",
    startAt: 0,
    autoplay: 4000,
    gap: 0,
    hoverpause: true,
    perView: 1,
    animationDuration: 800,
    animationTimingFunc: "linear",
  }).mount();
}

//Owl Carousel
$('#slider1').owlCarousel({
  loop: true,
  margin: 10,
  autoplay:true,
  autoplayHoverPause: true,
  responsive: {
      0: {
          items: 2,
          nav: false,
        },
        868: {
          items: 3,
          nav: false,
        },
        1136: {
          items: 4,
          nav: false,
        },
        1600: {
          items: 5,
          nav: false,
        }
  }
})