
$(document).ready(function(){

    $(".display-category-form-button").click(function(){
        var cat_id = $(this).attr('id')
        $(`#add-product-to-${cat_id}`).toggle(500)
        console.log($(this).html())
        if ($(this).html() == "Add product to this category"){
            $(this).html("Close form")
        } else {
            $(this).html("Add product to this category")
        }
    })

    $(".edit-product-btn").click(function(){
        var prod_id = $(this).attr('id')
        $(`#product-edit-div-${prod_id}`).toggle(300)
        console.log($(this).html())
        if ($(this).html() == "EDIT"){
            $(this).html("Close without save")
        } else {
            $(this).html("EDIT")
        };
    })

    $(".edit-category-btn").click(function(){
        var cat_id = $(this).attr('id');
        console.log(cat_id);
        $(`#edit-category-${cat_id}`).toggle(300);
        if ($(this).html() == "EDIT"){
            $(this).html("Close without save")
        } else {
            $(this).html("EDIT")
    }
    });
    $("#get-clients-btn").click(function(){
        $('.fetched-client-detail').remove()
        var searched_first_name = $('#client-first-name').val()
        if (searched_first_name == ""){
            console.log('ok')
            searched_first_name = "none"
        }
        var searched_last_name = $('#client-last-name').val()
        if (searched_last_name == ""){
            console.log('kok')
            searched_last_name = "none"
        }
        console.log(searched_first_name, searched_last_name)
        $.ajax({
            type: "GET",
            url: `${clients_url}${searched_first_name}/${searched_last_name}`,
        }).done(function(response){
            if (response.length > 0){
                for (i=0; i < response.length; i++){
                    $('#fetched-clients').append(`
                    
                    <div class="fetched-client-detail row"><hr>
                        <div class="col-sm-4">
                        ${response[i].first_name}  ${response[i].last_name}
                        </div>
                        <div class="col-sm-4">
                            <a href="${base_url}home_invite/${response[i].id}/${home}" class="btn btn-success">
                            INVITE
                            </a>
                        </div>
                    </div>
                </div>
                `)
                };
            } else {
                
                alert("Provide first name or last name to search")
            };
        });
    })
    


});

