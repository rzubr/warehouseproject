$(document).ready(function(){

    function GetProducts(){
        $.ajax({
            type: "GET",
            url: products_url,
        }).done(function(response){
            console.log(response)
            if (response.length > 0 ){
                for (i=0; i < response.length; i++){ // if product is requested:
                    if (response[i].status == 'R'){
                        $('#requested-products-list').append(`
                        <div id="list-product-${response[i].id}" class='row mt-2'>
                            <div class='col-sm-4'>
                                <p id='product-name-${response[i].id}'>${response[i].name}</p>
                            </div>
                            <div class='col-sm-2'>
                            <a id="status-product-${response[i].id}" class='status-change-btn col-sm-12 btn btn-success'>DONE</a>
                            </div>
                            <div class='col-sm-2'>
                                <a id="${response[i].id}-list-product" class='delete-product-btn col-sm-12 btn btn-danger'>DELETE</a>
                            </div>
                        </div>
                        `
                        );
                    } else { // if product is completed already
                        $('#requested-products-list').append(`
                        <div id="list-product-${response[i].id}" class='row mt-2'>
                            <div id='product-name-${response[i].id}' class='col-sm-4'>
                                <p style="text-decoration:line-through" id='product-name-${response[i].id}'>${response[i].name} </p>
                            </div>
                            <div class='col-sm-2'>
                            <a id="status-product-${response[i].id}" class="status-change-btn col-sm-12 btn btn-warning">REMOVE</a>
                        </div>
                            <div class='col-sm-2'>
                                <a id="${response[i].id}-list-product" class='delete-product-btn col-sm-12 btn btn-danger'>DELETE</a>
                            </div>
                        </div>
                    `)};
                };
            };
        }); 
    }// end of get products func

    GetProducts() 

    function DeleteProduct(product_id, list_id){
        $.ajax({
            type: "GET",
            url: base_delete_product_url+product_id+"/"+list_id
        }).done(function(response){
        })
    }; // end of delete product func


    function ChangeProductStatus(product_id, list_id){
        $.ajax({
            type: "GET",
            url: base_status_change_url+product_id+'/'+list_id
        }).done(function(response){

        })
    } //end of change product status function


    $('#requested-products-list').on('click', '.status-change-btn', function(){
        let product_id = $(this).attr('id')
        product_id = product_id.split('-')[2]
        ChangeProductStatus(product_id, list_pk)
        console.log('cyce')
        if ($(`#status-product-${product_id}`).html() == "REMOVE"){
            console.log(product_id)
            $(this).html("DONE").addClass('btn-success').removeClass('btn-warning')
            $(`#product-name-${product_id}`).css({'text-decoration' :''})
            
        } else {
            $(this).html("REMOVE").addClass('btn-warning').removeClass('btn-success')
            $(`#product-name-${product_id}`).css({'text-decoration' :'line-through'})
        }
        
        

    })


    $('#requested-products-list').on('click', '.delete-product-btn', function(){
        let product_id = $(this).attr('id')
        product_id = product_id.split('-')[0]
        DeleteProduct(product_id, list_pk)
        $(`#list-product-${product_id}`).fadeOut(800, function(){
            $(this).remove();

        })
    })





//end of ready function
});
    
