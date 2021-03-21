
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
    


});

