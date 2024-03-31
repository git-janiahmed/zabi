# forms.py
from django import forms
from .models import BookedEvent
from django.core.validators import RegexValidator

class BookedEventForm(forms.ModelForm):
    class Meta:
        model = BookedEvent
        fields = '__all__'  
        widgets = {                   
            'event_date': forms.TextInput(attrs={'class': 'text-sm text-gray-800 bg-white border rounded leading-5 py-4 px-4 md:py-2 md:px-2  border-gray-200 hover:border-gray-300 focus:border-indigo-300 shadow-sm placeholder-gray-400 focus:ring-0 w-full'}),
            'client_name': forms.TextInput(attrs={'class':"text-sm text-gray-800 bg-white border rounded leading-5 py-4 px-4 md:py-2 md:px-2 border-gray-200 hover:border-gray-300 focus:border-indigo-300 shadow-sm placeholder-gray-400 focus:ring-0 w-full"}),
            'phone': forms.TextInput(attrs={'class':"text-sm text-gray-800 bg-white border rounded leading-5 py-4 px-4 md:py-2 md:px-2 border-gray-200 hover:border-gray-300 focus:border-indigo-300 shadow-sm placeholder-gray-400 focus:ring-0 w-full"}),
            'num_people': forms.TextInput(attrs={'class':"text-sm text-gray-800 bg-white border rounded leading-5 py-4 px-4 md:py-2 md:px-2 border-gray-200 hover:border-gray-300 focus:border-indigo-300 shadow-sm placeholder-gray-400 focus:ring-0 w-full"}),
            'event_price': forms.TextInput(attrs={'class':"text-sm text-gray-800 bg-white border rounded leading-5 py-4 px-4 md:py-2 md:px-2 border-gray-200 hover:border-gray-300 focus:border-indigo-300 shadow-sm placeholder-gray-400 focus:ring-0 w-full"}),
            'razor_id': forms.TextInput(attrs={'class':"text-sm text-gray-800 bg-white border rounded leading-5 py-4 px-4 md:py-2 md:px-2 border-gray-200 hover:border-gray-300 focus:border-indigo-300 shadow-sm placeholder-gray-400 focus:ring-0 w-full"}),
        }

class PhoneSearchForm(forms.Form):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+919999999999'. Up to 15 digits allowed."
    )
    phone_number = forms.CharField(validators=[phone_regex], max_length=15)

    def __init__(self, *args, **kwargs):
        super(PhoneSearchForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget = forms.TextInput(attrs={'placeholder': 'Enter a valid Phone number', 'class': 'text-sm md:text-lg text-gray-800 bg-white border rounded leading-5 py-2 px-2  border-gray-200 hover:border-gray-300 focus:border-indigo-300 shadow-sm placeholder-gray-400 focus:ring-0 w-full'})

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100, widget=forms.TextInput(attrs={"class": "peer w-full rounded border border-gray-700 bg-gray-800 bg-opacity-40 py-1 px-3 text-base leading-8 text-gray-100 placeholder-transparent outline-none transition-colors duration-200 ease-in-out focus:border-indigo-500 focus:bg-gray-900 focus:ring-2 focus:ring-indigo-900"}))
    email = forms.EmailField(label='Your Email', max_length=100, widget=forms.EmailInput(attrs={"class": "peer w-full rounded border border-gray-700 bg-gray-800 bg-opacity-40 py-1 px-3 text-base leading-8 text-gray-100 placeholder-transparent outline-none transition-colors duration-200 ease-in-out focus:border-indigo-500 focus:bg-gray-900 focus:ring-2 focus:ring-indigo-900"}))
    message = forms.CharField(label='Your Message', widget=forms.Textarea(attrs={'class': 'peer h-32 w-full resize-none rounded border border-gray-700 bg-gray-800 bg-opacity-40 py-1 px-3 text-base leading-6 text-gray-100 placeholder-transparent outline-none transition-colors duration-200 ease-in-out focus:border-indigo-500 focus:bg-gray-900 focus:ring-2 focus:ring-indigo-900'}))
