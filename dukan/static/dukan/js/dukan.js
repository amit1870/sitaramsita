function view_products(category_id){
    $.ajax(
    {
        type:"GET",
        url: "/categorys/" + category_id,
        success: function( data ) 
        {
            $("div[id^='product_id_']").attr('style','display:none !important');

            $.each(data, function(index, product){
                    $( '#product_id_' + product.pk ).css("display","block");
            });
        }
     })
}

function calculate_amount(product_id, avl_qty, cost) {
    var order_qty = $("input[id^='order_qty_" + product_id + "']").val();
    var prod_total = order_qty * cost;
    $("span[id^='amount_" + product_id + "']").html('&#8377;' + prod_total);

    // $("span[id^='amount_" + product_id + "']").text(total);
    var order_total = 0;
    $("span[id^='amount_").each(function(){
        var prod_total = $(this).text();
        prod_total = prod_total.slice(1)
        order_total = order_total + parseFloat(prod_total);
    });
    $("strong[id^='total_strong']").html('&#8377;' + order_total);
}