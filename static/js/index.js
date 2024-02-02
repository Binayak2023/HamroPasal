//Jquery code
//NavBar
$(()=>{
  $(window).on("scroll", ()=>{
   if ($(window).scrollTop() > 150) {
    $('.cartpopup').addClass('cartpopup-scrolled');
  } else {
    $('.cartpopup').removeClass('cartpopup-scrolled');
   }
  })
})

//Search PopUp
$(()=>{
  $('.search-icon').on('click', ()=>{
    $('.search-popup').addClass('search-popup-open');
  })
  $('.search-popup .exit').on('click', ()=>{
    $('.search-popup').removeClass('search-popup-open');
  })
})

//Cart Popup
$(()=>{
  setTimeout(
    $('.initialbutton').on('click', function(){
      $('.cartpopup').slideDown();

      $(`.cartpopupexit span`).on('click', function(){
        $('.cartpopup').fadeOut();
      });
  }), 1000);
})

//Message Popup
$(()=>{
  $('.show-message-popup').on('click',function(e){
    e.preventDefault();
    $('.message-popup').css({'visibility':'visible','opacity':'1'});
    setTimeout(function(){
      $('.message-popup').css({'visibility':'hidden','opacity':'0'});
    }, 1500);
    $('.hide-message-popup').on('click', function(){
      $('.message-popup').css({'visibility':'hidden','opacity':'0'});
    })
  })
})

//Checkout Address Form
$(()=>{
  $('.another-address').on('click', function(){
    $('.payment .customer-form').slideToggle();
    if ($(this).children('button').html() == 'Cancel') {
      $(this).children('button').html('<i class="fas fa-plus-circle"></i> Add new address')
    } else {
      $(this).children('button').html('Cancel')
    }
  })
})

// Checkout Submit
$(()=>{
  let val =  $('input:radio[name=address]:checked').val();
  if ( !val) {
    $('#selectaddress').text('Please select an address')
    $('.checkout-submit').attr('disabled', true);
    $('.checkout-submit').css('cursor', 'not-allowed')
  } else {
    $('#selectaddress').text('')
    $('.checkout-submit').attr('disabled', false)
    $('.checkout-submit').css('cursor', 'pointer')
  }
  $('input:radio[name=address]').on('click', function(){
    $('#selectaddress').text('')
    $('.checkout-submit').attr('disabled', false)
    $('.checkout-submit').css('cursor', 'pointer')
  })
})

$(()=>{
  let can = $('.checkout-subimt').attr('disabled')
})