// Wishlist
$(()=>{
    let wishcount = parseInt($('.wishlistcounter').text())
    $('.addToWishlist').on('click', function(e){
        e.preventDefault();
        url = $(this).attr('data-url')
        prod_id = $(this).attr('data-id')
        $.ajax({
            type: "POST",
            url : url,
            data:{
                prod_id:prod_id
            },
            success: function(response){
                if (response.message === 'added') {
                    $('.addToWishlist').html('Remove Form Favorites')
                    wishcount = wishcount + 1
                } else {
                    wishcount = wishcount - 1
                    $('.addToWishlist').html('Add To Favorites')
                }
                $('.wishlistcounter').text(wishcount);
                $('.mobilewishlistcounter').text(wishcount);
            },
            error:function(response){
                console.log('Error: ', response)
            }
        })
    })
})