from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.urls import path
from django.contrib.auth.models import User
from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
    DateRangeQuickSelectListFilterBuilder,
)
from .models import Event, TimeSlot, BookedEvent, History, ContactMessage

class CustomAdminSite(admin.AdminSite):
    site_header = 'HappyTyms administration'
   
class TimeSlotAdmin(admin.ModelAdmin):
    search_fields = ('slot_number', 'event__title')
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if isinstance(db_field, models.TimeField):
            formfield.widget = admin.widgets.AdminTimeWidget(format='%I:%M %p')
        return formfield


class BookedEventAdmin(admin.ModelAdmin):
    # actions on querysets at dashboard
    actions = ['delete_objects_with_filter', 'move_objects_to_history_model']
   
    def delete_objects_with_filter(self, request, queryset):
        # Apply your filter condition here
        filtered_queryset = queryset.filter(status='created')

        # Delete objects matching the filter
        count, _ = filtered_queryset.delete()
        self.message_user(request, f"{count} objects with unpaid status deleted successfully.")
    
    def move_objects_to_history_model(self, request, queryset):
        count = 0
        for event in queryset:
            history_entry =  History.objects.create(
                event=event.event, 
                event_date=event.event_date,
                slot=event.slot, 
                client_name=event.client_name,
                phone=event.phone,
                num_people=event.num_people,
                
                event_price = event.event_price,
                razor_id = event.razor_id,
                amount_paid = event.amount_paid,
                amount_due = event.amount_due,
                created_at = event.created_at,
                status = event.status,
                attempt = event.attempt
            )
            history_entry.save()
            event.delete()
            count+= 1

        self.message_user(request, f"{count} completed objects moved to History and deleted from here.")

    move_objects_to_history_model.short_description = "Move selected objects to history and delte from here"
    delete_objects_with_filter.short_description = "Delete all unpaid status objects"



    list_display = ('client_name', 'phone', 'booking_date', 'event', 'event_date', 'slot', 'event_price', 'num_people', 'razor_id', 'amount_paid', 'amount_due', 'created_at', 'status', 'attempt')
    list_filter = (
        ("event_date", DateRangeFilterBuilder(
            title="Search By Event Date"
        )),
        (
            "booking_date",
            DateRangeFilterBuilder(
                title="Search By Booking Date",
                
            ),
        ),
        ("event_price", NumericRangeFilterBuilder(
            title="Search By Price Range"
        )),
        'status'
          
    )
    search_fields = ('client_name', 'phone')
    ordering = ('-booking_date',)
    class Media:
       js = ('https://code.jquery.com/jquery-3.6.0.min.js', 'js/admin_custom.js',)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('process-selected-event/', self.process_selected_event),
            path('calculate-price/', self.calculate_price)
        ]
        return custom_urls + urls

    def process_selected_event(self, request):
        if request.method == 'POST':
           

            selected_event_id = request.POST.get('event_id')
            if selected_event_id is None or selected_event_id == '':
                return JsonResponse({'error': 'Invalid event ID'})
            try:
                # Retrieve the event object using the received event ID
                event = Event.objects.get(pk=selected_event_id)
                # Access the desired fields from the event object
                price = event.price
                maxPeople = event.maxPeople
                
                slots = TimeSlot.objects.filter(event=event)
                serialized_slots = [{
                    'id': slot.id,
                    'text': f"{event.title} - Slot {slot.slot_number}: {slot.formatted_start_time()} to {slot.formatted_end_time()}"
                } for slot in slots]
                # Get the help text for num_people field
                num_people_help_text = self.model._meta.get_field('num_people').help_text
                # Append the maximum number of people to the help text
                num_people_help_text += f" (Maximum Guest will be: {maxPeople}) for an extra person 100INR will be charged"
                # Return the price, num_people, and help text values in the JSON response
                return JsonResponse({
                    'price': price,
                    'num_people': maxPeople,
                    'num_people_help_text': num_people_help_text,
                    'slots': serialized_slots
                    
            })
            except Event.DoesNotExist:
                return JsonResponse({'error': 'Event does not exist'})
        else:
            return JsonResponse({'error': 'Invalid request method'})
    def calculate_price(self, request):
        if request.method == 'POST':
            event_id = request.POST.get('event_id')
            num_people = int(request.POST.get('num_people', 0))
            
            try:
                event = Event.objects.get(pk=event_id)
                base_price = event.price
                extra_charge_per_person = 100
                extra_people_count = max(num_people - event.maxPeople, 0)
                total_price = base_price + extra_people_count * extra_charge_per_person

                return JsonResponse({'total_price': total_price})
            except Event.DoesNotExist:
                return JsonResponse({'error': 'Event does not exist'})
        else:
            return JsonResponse({'error': 'Invalid request method'})
            
class HistoryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Disable the ability to add new events
        return False
    def has_change_permission(self, request, obj=None):
        # Disable the ability to change existing events
        return False
    list_display = ('client_name', 'phone', 'booking_date', 'event', 'event_date', 'slot', 'event_price', 'num_people')
    list_filter = (
        ("event_date", DateRangeFilterBuilder(
            title="Search By Event Date"
        )),
        (
            "booking_date",
            DateRangeFilterBuilder(
                title="Search By Booking Date",
                
            ),
        ),
        ("event_price", NumericRangeFilterBuilder(
            title="Search By Price Range"
        )),
          
    )
    search_fields = ('client_name', 'phone') 


admin_site = CustomAdminSite()

admin_site.register(User)
admin_site.register(Event)
admin_site.register(ContactMessage)

admin_site.register(History, HistoryAdmin)
admin_site.register(TimeSlot, TimeSlotAdmin)
admin_site.register(BookedEvent, BookedEventAdmin)




