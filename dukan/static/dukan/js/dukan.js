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