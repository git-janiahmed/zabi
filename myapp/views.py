import requests, json, razorpay
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.conf import settings
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from .forms import PhoneSearchForm, BookedEventForm, ContactForm
from .models import Event, BookedEvent, ContactMessage

# importing razor pay API from settings
client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))


class termsndConditions(TemplateView):
    template_name = 'terms.html'

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = ContactForm()  
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if email already exists in database
            if ContactMessage.objects.filter(email=email).exists():
                return JsonResponse({'message': 'You have already submitted a message. Please wait until we reply.'})
            else:
                name = form.cleaned_data['name']
                message = form.cleaned_data['message']
                ContactMessage.objects.create(name=name, email=email, message=message)
                return JsonResponse({'message': 'Your message has been submitted successfully! We will get back to you soon.'})
        return JsonResponse({'message': 'Form submission failed. Please check the form and try again.'}, status=400)
   
class bookNow(DetailView):
    model = Event
    cards = Event.objects.all()
    template_name = 'bookNow.html'
    context_object_name = 'card'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        content_list = event.content.split('\n')
        context['content_list'] = content_list
        default_values = {
        'event': event,
        
        # Add more fields and their default values as needed
    }
        bookingForm = BookedEventForm(initial=default_values)
        context['booking_form'] = bookingForm

        return context
    
    def post(self, request, *args, **kwargs):
        event = self.get_object() 
        form = BookedEventForm(request.POST)  
        action = request.POST.get('action')  
        
        if action == 'delete':
            event_pk = request.POST.get('pk')
            try:
                obj = BookedEvent.objects.get(pk=event_pk)
                obj.delete()
                return JsonResponse({'message': 'Object deleted successfully'})
            except BookedEvent.DoesNotExist:
                return JsonResponse({'error': 'Object not found'}, status=404)

        if form.is_valid():
            booked_event = form.save(commit=False)
            # Check if the booked event already exists for the given event date and slot
            if BookedEvent.objects.filter(event=event, event_date=booked_event.event_date, slot=booked_event.slot).exists():
                return JsonResponse({'error': 'This time slot is already booked for the specified event date'}, status=400)

            try:
                booked_event.clean()  
            except ValidationError as e:
                # Serialize validation errors
                errors = dict()
                for field, error in e.message_dict.items():
                    errors[field] = list(error)
                return JsonResponse({'error': errors}, status=400)
            booked_event.event_price = booked_event.calculate_price()
            order = create_order(booked_event.event_price, booked_event.pk,booked_event.event_date)
            try:
                booked_event.razor_id = order['id']
                booked_event.amount_paid = order['amount_paid']
                booked_event.amount_due = order['amount_due'] 
                booked_event.created_at = order['created_at']
                booked_event.status = order['status']
                booked_event.attempt = order['attempts']
            except Exception as e:
               print(e)


            booked_event.save()
            event_json = serialize('json', [booked_event])
            
            
            # Optionally, you can return success response
            return JsonResponse({'success': 'Event is booked for you', "order": order, "event": event_json,})

        # Form data is invalid
        errors = form.errors.as_json()
        return JsonResponse({'error': errors}, status=400)

class SearchDetailView(TemplateView):
    template_name = 'search.html'
    model = BookedEvent
    form_class = PhoneSearchForm  # Corrected attribute name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Call the superclass method to get the initial context
        
        # Instantiate the form with GET data
        searchForm = self.form_class(self.request.GET)
        context['search_form'] = searchForm  # Add the form to the context

        # If the form is valid, filter BookedEvent instances by phone number
        if searchForm.is_valid():
            phone_number = searchForm.cleaned_data['phone_number']
            search_result = BookedEvent.objects.filter(phone=phone_number)
            context['booked_events'] = search_result  # Add search results to the context

        return context

def send_whatsapp_message_view(request):
    recipient_number = '923238599108'  # Replace with the recipient's phone number
    message = 'Hello, this is a test message from my Django app!'
    access_token = settings.FACEBOOK_ACCESS_TOKEN

    # Construct the request
    url = 'https://graph.facebook.com/v18.0/257569127443314/messages'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
        "code": "en_US"
    }
        },
        
        
    }

    # Send the request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Return the response
    return JsonResponse(response.json())
   
def create_order(amount, pk, date):
    data = {
         
        'amount': amount*100,
        'currency': "INR",
        "receipt": str(pk)+str(date)
       
    }
    return client.order.create(data=data)

@csrf_exempt
def fetch_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            # Assuming `fetch_order` is defined somewhere
            order = client.order.fetch(order_id)
            # Process the order as needed
            return JsonResponse({'message': 'Order fetched successfully', 'order': order})
        else:
            return JsonResponse({'error': 'Order ID not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def update_price_at_bookedEvent(request):
    if request.method == 'POST':
        received_data = request.POST  # Assuming data is sent via POST
        
        # Check if 'id' exists in the received_data
        if 'id' in received_data:
            
            try:
                # Fetch the existing BookedEvent instance
                booked_event = BookedEvent.objects.get(razor_id=received_data['id'])
                
                # Divide the amount paid by 100
                amount_paid = int(received_data['amount_paid']) / 100
                
                # Update the BookedEvent instance
                BookedEvent.objects.filter(razor_id=received_data['id']).update(
                    status=received_data['status'],
                    attempt=received_data['attempts'],
                    amount_paid=amount_paid,  # Updated amount_paid value
                    amount_due=received_data['amount_due']
                )
                
                return JsonResponse({'success': 'Model instance updated successfully'})
            except BookedEvent.DoesNotExist:
                return JsonResponse({'error': 'BookedEvent with the provided razor_id does not exist'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'No id provided in the received data'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)







