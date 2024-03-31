$(document).ready(function () {
    $("#id_num_people").on("change", function() {
        $("#id_event_price").trigger("change");
    });
    $('.loading2').addClass('hidden')
    $("#id_event").trigger("change");
    $('.after-pay').addClass('hidden')
    $('#id_event').addClass(
        'block w-full bg-white border p-4 md:p-2 border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500'
    );
    $('#id_slot').addClass(
        'block w-full bg-white border p-4 md:p-2 border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-indigo-500'
    );

});
$("#rzp-button1").hide();
let eventData;




function submitForm() {
    var form = $('#booking-form');
    var errorMessage = '';
    var successMessage = '';
    $('.loading2').removeClass('hidden')

    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        dataType: 'json',

        success: function (response) {
            $('.loading2').addClass('hidden')

            $('#booking-error').text('').hide();
            if (response.success) {
                $('#booking-form').remove()
                successMessage = response.success;
                $("#rzp-button1").show();
                const getOrder = response.order
                const event = JSON.parse(response.event)
                eventData = event[0];

                $('.event-detail').append(`
                <div class='text-lg my-4 font-bold'><span class='text-red-600'>Please pay us to keep your reservation.</span><span class='text-sm'>your reservation automatically deleted if you not pay</div>
                
               <div class='flex gap-8 py-2'><h1>Your Resvered Date:</h1><span class="text-gray-500">${eventData.fields.event_date}</span></div>
                <div class='flex gap-8 py-2'><h1>Payment Status:</h1><span class="text-gray-500">${eventData.fields.status}</span></div>
                <div class='flex gap-8 py-2'><h1>Amount Due:</h1><span class="text-gray-500">${eventData.fields.event_price}</span></div>
                  
                `);
                
                $('#booking-success').removeClass('hidden');
                $('#booking-error').addClass("hidden");
                $('#delete-btn').removeClass("hidden");
                $('#rzp-button1').removeClass('hidden')
                $('#booking-success').text(successMessage).show();
                var options = {
                    "key": "rzp_test_rjozYzFtHN9E9n", // Enter the Key ID generated from the Dashboard
                    "amount": getOrder
                        .amount, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                    "currency": "INR",
                    "name": "Happy Tyms",
                    "description": `Payment for booking event`,
                    "image": "../../static/img/icon.png",

                    "order_id": getOrder
                        .id, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                    "handler": function (response) {
                        function getCSRFToken() {
                            return $('input[name="csrfmiddlewaretoken"]').val();
                        }

                        $.ajax({
                            type: "POST",
                            url: "/fetch/payments/order",

                            data: {
                                'order_id': response.razorpay_order_id
                            },
                            success: function (response) {
                                const order = response.order
                                
                                $.ajax({
                                    type: "POST",
                                    url: "/update-price/model/bookedevent", // URL for updating the model
                                    data: {
                                        // Pass the received data to update the model
                                        'attempts': response.order
                                            .attempts,
                                        'id': response.order.id,
                                        "status": response.order.status,
                                        "amount_due": response.order
                                            .amount_due,
                                        "amount_paid": response.order
                                            .amount_paid,

                                        // Add more fields if needed
                                    },
                                    headers: {
                                        "X-CSRFToken": getCSRFToken() // Include CSRF token in headers
                                    },
                                    success: function (updateResponse) {
                                        // Handle success of model update
                                       
                                        $('#booking-form').remove()
                                        $("#delete-btn").remove();
                                        $(".event-detail").remove();

                                        $("#rzp-button1").remove();

                                        
                                        $('#booking-success').append(`<span>Congratulations! Your event booking is confirmed.🎉</span><br><span>Thank you for choosing Us! We look forward to hosting you at the event.</span>`)

                                        $('#success-payment').append(
                                            ` <div class='flex gap-8 py-2'><h1>Razor Id:</h1><span class="text-gray-500">${order.id}</span></div>
                <div class='flex gap-8 py-2'><h1>Payment Status:</h1><span class="text-gray-500">${order.status}</span></div>
                <div class='flex gap-8 py-2'><h1>Amount Due:</h1><span class="text-gray-500">${order.amount_due}</span></div>
             `
                                        )

                                        $('.after-pay').removeClass('hidden')

                                    },
                                    error: function (xhr, status,
                                        error) {
                                        // Handle error
                                       
                                    }
                                });
                            },
                            error: function (xhr, errmsg, err) {
                                // Handle error
                            }
                        });
                        // alert(response.razorpay_payment_id);
                        // alert(response.razorpay_order_id);
                        // alert(response.razorpay_signature)
                    },
                    // "prefill": {
                    //     "name": eventData.fields.client_name,

                    //     "contact": eventData.fields.phone
                    // },
                    // "notes": {
                    //     "address": "Razorpay Corporate Office"
                    // },
                    "theme": {
                        "color": "#3399cc"
                    }
                };
                var rzp1 = new Razorpay(options);
                rzp1.on('payment.failed', function (response) {
                    alert(response.error.code);
                    alert(response.error.description);

                    alert(response.error.reason);

                });
                document.getElementById('rzp-button1').onclick = function (e) {
                    rzp1.open();
                    e.preventDefault();
                }

                // Optionally, reset the form or do any other actions
                form.trigger('reset');
            } else {
               
            }
        },
        error: function (xhr, status, error) {
            // Clear success message
            $('.loading2').addClass('hidden')
            $('#booking-success').text('').hide();
            $('#booking-success').addClass('hidden');
            

            try {


                var jsonResponse = JSON.parse(xhr.responseText);

                $('#booking-error').text(jsonResponse.error).show();

              
                $('#booking-error').removeClass('hidden');
                $("#rzp-button1").hide();

            } catch (e) {


            }

        }
    });
    return false; // Prevent default form submission
}