from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import RegexValidator

class Event(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(help_text="Write the details for the event separated by line")
    price = models.PositiveIntegerField()
    img = models.ImageField(upload_to="card_field/", help_text="THis is the cover pictuer and required")
    img2 = models.ImageField(upload_to="card_field/", blank=True, null=True)
    img3 = models.ImageField(upload_to="card_field/", blank=True, null=True)
    img4 = models.ImageField(upload_to="card_field/", blank=True, null=True)
    img5 = models.ImageField(upload_to="card_field/", blank=True, null=True)
    maxPeople = models.PositiveIntegerField(default=1)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not isinstance(self.price, int) or self.price < 0:
            raise ValidationError("Price must be a positive integer.")
        self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class TimeSlot(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    slot_number = models.PositiveIntegerField(default=1)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('event', 'slot_number')

    def formatted_start_time(self):
        return self.start_time.strftime('%I:%M %p')

    def formatted_end_time(self):
        return self.end_time.strftime('%I:%M %p')

    def __str__(self):
        return f"{self.event.title} - Slot {self.slot_number}: {self.formatted_start_time()} to {self.formatted_end_time()}"

class History(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_date = models.DateField()
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    client_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    num_people = models.PositiveIntegerField(default=1, help_text="|")
    event_price = models.PositiveBigIntegerField(default=0)
    event_price = models.PositiveBigIntegerField(default=0)
    razor_id = models.CharField(max_length=100, default=0, null=True, blank=True)
    amount_paid = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    amount_due = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    created_at = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    status = models.CharField(max_length=100, default=0, null=True, blank=True)
    attempt = models.PositiveBigIntegerField(default=0, null=True, blank=True)

   

    def __str__(self):
        return f"{self.event.title} - {self.event_date} - Slot {self.slot.slot_number}"

class BookedEvent(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+919999999999'. Up to 15 digits allowed."
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    event_date = models.DateField()
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    client_name = models.CharField(max_length=100)
    phone = models.CharField(validators=[phone_regex], max_length=100)
    num_people = models.PositiveIntegerField(default=1, help_text="|")
    event_price = models.PositiveBigIntegerField(default=0)
    razor_id = models.CharField(max_length=100, default=0, null=True, blank=True)
    amount_paid = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    amount_due = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    created_at = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    status = models.CharField(max_length=100, default=0, null=True, blank=True)
    attempt = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    def clean(self):
        super().clean()
        if self.event_date is not None and self.event_date < timezone.now().date():
            raise ValidationError('Reservation date cannot be in the past.')
        if not self.is_available():
            raise ValidationError('This time slot is already booked for the specified event date.')

    def is_available(self):
        return not BookedEvent.objects.filter(event=self.event, event_date=self.event_date, slot=self.slot).exists()

    def calculate_price(self):
        base_price = self.event.price
        extra_charge_per_person = 100
        extra_people_count = max(self.num_people - self.event.maxPeople, 0)
        total_price = base_price + extra_people_count * extra_charge_per_person
        return total_price

    def save(self, *args, **kwargs):
        if self.is_available():
            self.amount_paid /= 100
            self.amount_due /= 100
            self.event_price = self.calculate_price()
            super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.client_name} | {self.phone} | {self.booking_date} | {self.slot}"
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

        