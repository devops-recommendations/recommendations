$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#id").val(res.id);
        $("#product_id").val(res.product_id);
        $("#rec_product_id").val(res.rec_product_id);
        $("#type").val(res.type);
        if (res.type == 0) {
            $("#type").val("Generic");
        } else if (res.type == 1) {
            $("#type").val("BoughtTogether");
        } else if (res.type == 2) {
            $("#type").val("CrossSell");
        } else if (res.type == 3) {
            $("#type").val("UpSell");
        } else if (res.type == 4) {
            $("#type").val("Complementary");
        }
        $("#interested").val(res.interested);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#id").val("");
        $("#product_id").val("");
        $("#rec_product_id").val("");
        $("#type").val("");
        $("#interested").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Recommendations
    // ****************************************

    $("#create-btn").click(function () {

        var prodcut_id = $("#product_id").val();
        var rec_product_id = $("#rec_product_id").val();
        var type = $("#type").val();

        var data = {
            "product_id": prodcut_id,
            "rec_product_id": rec_product_id,
            "type": type
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/recommendations",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Recommendations
    // ****************************************

    $("#update-btn").click(function () {

        var id = $("#id").val();
        var product_id = $("#product_id").val();
        var rec_product_id = $("#rec_product_id").val();
        var type = $("#type").val();

        var data = {
            "product_id": product_id,
            "rec_product_id": rec_product_id,
            "type": type
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/recommendations/" + id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a recommendation
    // ****************************************

    $("#retrieve-btn").click(function () {

        var id = $("#id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/recommendations/" + id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Recommendation
    // ****************************************

    $("#delete-btn").click(function () {

        var id = $("#id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/recommendations/" + id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Pet has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Increase a Intersted Count
    // ****************************************

    $("#interested-btn").click(function () {

        var id = $("#id").val();

        var ajax = $.ajax({
            type: "PUT",
            url: "/recommendations/" + id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });



    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Recommendation
    // ****************************************

    $("#search-btn").click(function () {

        var product_id = $("#product_id").val();
        var rec_product_id = $("#rec_product_id").val();
        var type = $("#type").val();

        var queryString = ""

        if (product_id) {
            queryString += 'product_id=' + product_id
        }
        if (rec_product_id) {
            if (queryString.length > 0) {
                queryString += '&rec_product_id=' + rec_product_id
            } else {
                queryString += 'rec_product_id=' + rec_product_id
            }
        }
        if (type) {
            if (queryString.length > 0) {
                queryString += '&type=' + type
            } else {
                queryString += 'type=' + type
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/recommendations?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:20%">Product ID</th>'
            header += '<th style="width:30%">Recommendation Product ID</th>'
            header += '<th style="width:20%">Type</th>'
            header += '<th style="width:20%">Interested Count</th></tr>'

            $("#search_results").append(header);
            var firstRecommendation = "";
            for(var i = 0; i < res.length; i++) {
                var recommendation = res[i];
                var row = "<tr><td>"+recommendation.id+"</td><td>"+recommendation.product_id+"</td><td>"+recommendation.rec_product_id+"</td><td>"+recommendation.type+"</td></tr>"recommendation.interested+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstRecommendation = recommendation;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstRecommendation != "") {
                update_form_data(firstRecommendation)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
