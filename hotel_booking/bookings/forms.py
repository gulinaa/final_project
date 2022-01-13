from django import forms
from datetime import datetime

from .models import Booking


class BookingForm(forms.ModelForm):
    created = forms.DateTimeField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), required=False)

    class Meta:
        model = Booking
        exclude = ('user', )
