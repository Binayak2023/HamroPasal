//To check if products exists in cart
$(()=>{
    if ($('.cart table tr#carttablerow').length <= 1) {
        $('a.checkout').on('click', function(e){
            e.preventDefault();
        })
    }
})

//For add and subtract button
$(()=>{
    let prodSubTotalText = $('.prodOnlyTotal')
    let prodSubTotal = parseFloat(prodSubTotalText.text().slice(3))
    $('.initialbutton, .plusbutton, .minusbutton').on('click', function(e){
        e.preventDefault();
        let prod_id = $(this).attr('data-id');
        let prod_url = $(this).attr('data-url');
        let data_table_id = $(this).parent().parent().parent().attr('data-table-id');

        $.ajax({
            method: "POST",
            url : prod_url,
            data : {
                prod_id: prod_id,
                quantity: 1,
            },
            success: function(response){
                if (response.action == 'subt' && response.proqty == 0){
                    $(`.datatableid${data_table_id}`).fadeOut();
                    $(`.mb${prod_id}`).fadeOut(1);
                    $(`.bt${prod_id}`).text(response.proqty).fadeOut(1);
                    $(`.pb${prod_id}`).fadeOut(1);
                    $(`.ib${prod_id}`).slideDown();
                    prodSubTotal -= response.selling_price
                    prodSubTotalSub = `Rs.${prodSubTotal}.0`
                    $('.prodOnlyTotal').text(prodSubTotalSub)
                    cartproducts  = response.cartproducts
                    popupsubtotal = 0
                    $('.cartpopupprodcontainer').empty();
                    Object.entries(cartproducts).forEach(function(key){
                        popupsubtotal +=key[1].prod_price * key[1].prod_quantity
                        $('.cartpopupprodcontainer').append(` <div class="cartpopupprod cartpopupprod${key[1].prod_id}" data-prod-id="${key[1].prod_id}" data-delete-url="/delete-from-cart/">
                        <img src="${key[1].prod_image_url}" alt="">
                        <div class="cartpopupproddesc">
                        <p><a href=""><strong>${key[1].prod_name}</strong></a></p>
                        <p>${key[1].prod_weight}</p>
                        <p>${key[1].prod_quantity} * Rs.${key[1].prod_price}</p>
                        </div>
                        <div class="cartpopupprodremove">
                        <button class="popupDeleteCart"><i class="bx bx-trash" style="margin-top: 12px;"></i></button>
                        </div>
                        </div>`);
                    });
                    $(`.cartpopupprod${response.product_id}`).fadeOut();
                    $('.cartpopupprodsubtotal p strong').text('Sub Total: Rs.'+popupsubtotal + '.0')

                }else if(response.action == 'subt'){
                    $(`.ib${prod_id}`).slideUp(1);
                    $(`.mb${prod_id}`).fadeIn();
                    $(`.bt${prod_id}`).text(response.proqty).fadeIn();
                    $(`.pb${prod_id}`).fadeIn();
                    $(`.datatableid${data_table_id} td:last-child`).text(`Rs.${response.sub_total}`);
                    prodSubTotal -= response.selling_price
                    prodSubTotalSub = `Rs.${prodSubTotal}.0`
                    $('.prodOnlyTotal').text(prodSubTotalSub)
                    cartproducts  = response.cartproducts
                    popupsubtotal = 0
                    $('.cartpopupprodcontainer').empty();
                    Object.entries(cartproducts).forEach(function(key){
                        popupsubtotal +=key[1].prod_price * key[1].prod_quantity
                        $('.cartpopupprodcontainer').append(` <div class="cartpopupprod cartpopupprod${key[1].prod_id}" data-prod-id="${key[1].prod_id}" data-delete-url="/delete-from-cart/">
                        <img src="${key[1].prod_image_url}" alt="">
                        <div class="cartpopupproddesc">
                        <p><a href=""><strong>${key[1].prod_name}</strong></a></p>
                        <p>${key[1].prod_weight}</p>
                        <p>${key[1].prod_quantity} * Rs.${key[1].prod_price}</p>
                        </div>
                        <div class="cartpopupprodremove">
                        <button class="popupDeleteCart"><i class="bx bx-trash" style="margin-top: 12px;"></i></button>
                        </div>
                        </div>`);
                    });

                    $('.cartpopupprodsubtotal p strong').text('Sub Total: Rs.'+popupsubtotal + '.0')
                    let popupProdSubTotalText = $('.cartpopupprodsubtotal p strong')
                    let popupProdSubTotal = parseFloat(popupProdSubTotalText.text().slice(14))

                    $('.popupDeleteCart').on('click', function(){
                        popupProdId = $(this).parent().parent().attr('data-prod-id');
                        popupProdUrl = $(this).parent().parent().attr('data-delete-url');
                        $(`.datatableid${data_table_id}`).fadeOut();
                        $(`.mb${popupProdId}`).fadeOut(1);
                        $(`.bt${popupProdId}`).text(response.proqty).fadeOut(1);
                        $(`.pb${popupProdId}`).fadeOut(1);
                        $(`.ib${popupProdId}`).slideDown();
                        $.ajax({
                            method : "POST",
                            url : popupProdUrl,
                            data: {
                                prod_id: popupProdId
                            },
                            success: function(response){
                                $(`.cartpopupprod${response.rowId}`).fadeOut();
                                popupProdSubTotal -= response.prod_sub_total
                                $('.cartpopupprodsubtotal p strong').text('Sub Total: Rs.'+popupProdSubTotal + '.0')
                                $('.cartproductcount').text(response.cartproductcount);
                            },
                            error: function(response){
                                console.log('Error: ', response)
                            }
                        })
                    });


                }else if(response.action == 'add'){
                    $(`.ib${prod_id}`).slideUp(1);
                    $(`.mb${prod_id}`).fadeIn();
                    $(`.bt${prod_id}`).text(response.proqty).fadeIn();
                    $(`.pb${prod_id}`).fadeIn();
                    $(`.datatableid${data_table_id} td:last-child`).text(`Rs.${response.sub_total}`);
                    prodSubTotal += response.selling_price
                    prodSubTotalAdd = `Rs.${prodSubTotal}.0`
                    $('.prodOnlyTotal').text(prodSubTotalAdd)
                    cartproducts  = response.cartproducts
                    popupsubtotal = 0
                    $('.cartpopupprodcontainer').empty();
                    Object.entries(cartproducts).forEach(function(key){
                        popupsubtotal +=key[1].prod_price * key[1].prod_quantity
                        $('.cartpopupprodcontainer').append(` <div class="cartpopupprod cartpopupprod${key[1].prod_id}" data-prod-id="${key[1].prod_id}" data-delete-url="/delete-from-cart/">
                        <img src="${key[1].prod_image_url}" alt="">
                        <div class="cartpopupproddesc">
                        <p><a href=""><strong>${key[1].prod_name}</strong></a></p>
                        <p>${key[1].prod_weight}</p>
                        <p>${key[1].prod_quantity} * Rs.${key[1].prod_price}</p>
                        </div>
                        <div class="cartpopupprodremove">
                        <button class="popupDeleteCart"><i class="bx bx-trash" style="margin-top: 12px;"></i></button>
                        </div>
                        </div>`);
                    });
                    $('.cartpopupprodsubtotal p strong').text('Sub Total: Rs.'+popupsubtotal + '.0')

                    let popupProdSubTotalText = $('.cartpopupprodsubtotal p strong')
                    let popupProdSubTotal = parseFloat(popupProdSubTotalText.text().slice(14))


                    $('.popupDeleteCart').on('click', function(){
                        popupProdId = $(this).parent().parent().attr('data-prod-id');
                        popupProdUrl = $(this).parent().parent().attr('data-delete-url');
                        $(`.datatableid${data_table_id}`).fadeOut();
                        $(`.mb${popupProdId}`).fadeOut(1);
                        $(`.bt${popupProdId}`).text(response.proqty).fadeOut(1);
                        $(`.pb${popupProdId}`).fadeOut(1);
                        $(`.ib${popupProdId}`).slideDown();
                        $.ajax({
                            method : "POST",
                            url : popupProdUrl,
                            data: {
                                prod_id: popupProdId
                            },
                            success: function(response){
                                $(`.cartpopupprod${response.rowId}`).fadeOut();
                                popupProdSubTotal -= response.prod_sub_total
                                $('.cartpopupprodsubtotal p strong').text('Sub Total: Rs.'+popupProdSubTotal + '.0')
                                $('.cartproductcount').text(response.cartproductcount);
                            },
                            error: function(response){
                                console.log('Error: ', response)
                            }
                        })
                    });
                }

                else{
                    $(`.ib${prod_id}`).slideUp(1);
                    $(`.mb${prod_id}`).fadeIn();
                    $(`.bt${prod_id}`).text(response.proqty).fadeIn();
                    $(`.pb${prod_id}`).fadeIn();
                    $(`.datatableid${data_table_id} td:last-child`).text(`Rs.${response.sub_total}`);
                }
                $('.cartproductcount').text(response.cartproductcount);
            },
            error: function(response){
                console.log('Error:', response)
            }
        })
    })
})








// For Remove Button
$(()=>{
    let prodSubTotalText = $('.prodOnlyTotal')
    let prodSubTotal = parseFloat(prodSubTotalText.text().slice(3))
    $('.dataTable').on('click', function(e){
        e.preventDefault();
        const prodId = $(this).parent().parent().parent().parent().attr('data-table-id');
        const prodUrl = $(this).parent().parent().parent().parent().attr('data-table-url');
        $.ajax({
            method : "POST",
            url : prodUrl,
            data: {
                prod_id: prodId
            },
            success: function(response){
                $(`.datatableid${response.rowId}`).fadeOut();
                prodSubTotal -= response.prod_sub_total
                prodSubTotalAdd = `Rs.${prodSubTotal}.0`
                $('.prodOnlyTotal').text(prodSubTotalAdd)
                $('.cartproductcount').text(response.cartproductcount);
            },
            error: function(response){
                console.log('Error: ', response)
            }
        })
    })
});
