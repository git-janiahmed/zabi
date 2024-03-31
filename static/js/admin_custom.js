// admin_custom.js
(function($) {
    $(document).ready(function() {
        
        // Function to get CSRF token from cookie
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        $('#id_event_price').prop('readonly', true);
        $('#id_event').change(function() {
            var selectedEvent = $(this).val();
            
            
            // Get CSRF token
            var csrftoken = getCookie('csrftoken');
            // Perform AJAX call to send selectedEvent to the server
            $.ajax({
                
                url: '/admin/myapp/bookedevent/process-selected-event/',
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: { event_id: selectedEvent },
                success: function(response) {
                    // Handle success response from the server
                    
                    $('#num_people_help_text').text(response.num_people_help_text);
                    $('#id_slot').empty();
                    
                    $.each(response.slots, function(index, slot) {
                       
                        $('#id_slot').append($('<option>', {
                            value: slot.id,
                            text: slot.text  // Use slot.text to display the response
                        }));
                    });
                    // Update the price and num_people fields dynamically
                    $('#id_event_price').val(response.price);
                    
                    $('#id_num_people').val(response.num_people);
                    $('#id_num_people_helptext').text(response.num_people_help_text);
                    
                },
                error: function(xhr, status, error) {
                    // Handle error
                    
                }
            });
        });

        $('#id_num_people').change(function() {
            // Capture the new value of num_people
            var numPeople = $(this).val();


            // Perform AJAX call to calculate the total price based on num_people
            var selectedEvent = $('#id_event').val();
            var csrftoken = getCookie('csrftoken');
            $.ajax({
                url: '/admin/myapp/bookedevent/calculate-price/',
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: { 
                    event_id: selectedEvent,
                    num_people: numPeople
                },
                success: function(response) {
                    // Handle success response from the server
                    
                    // Update the event price field dynamically
                    $('#id_event_price').val(response.total_price);
                   
                },
                error: function(xhr, status, error) {
                    // Handle error
                   
                }
            });
        });
    });
})(jQuery);
