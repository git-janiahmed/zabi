from django.urls import path
from .views import HomeView, SearchDetailView, termsndConditions, bookNow, fetch_order, update_price_at_bookedEvent, send_whatsapp_message_view

urlpatterns = [
    
    path('', HomeView.as_view(), name='homePage'),
    path("fetch/payments/order", fetch_order, name='fetch_order'),
    path('booking/<slug:slug>/', bookNow.as_view(), name='booking'),
    path('search-my-bookedevents', SearchDetailView.as_view(), name='search'),
    path('terms_and_conditions/',  termsndConditions.as_view(), name='terms'),
    path('send-whatsapp-message/', send_whatsapp_message_view, name='send_whatsapp_message'),
    path('update-price/model/bookedevent', update_price_at_bookedEvent, name='update_event_price'),
 


     
]
