# context_processors.py

from .models import Event

def card_data(request):
    # Retrieve all card objects from the database
    cards = Event.objects.all()
    for card in cards:
        card.content = card.content.split('\n')
    # Return card data as a dictionary
    return {'cards': cards}
