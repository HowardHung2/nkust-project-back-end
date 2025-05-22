from django import forms
from .models import TripOrder

class PurchaseTripForm(forms.ModelForm):
    class Meta:
        model = TripOrder
        fields = ['spots_booked']
        labels = {
            'spots_booked': 'Number of People Booked',
        }
        widgets = {
            'spots_booked': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }

    def clean_spots_booked(self):
        spots = self.cleaned_data['spots_booked']
        if spots < 1:
            raise forms.ValidationError("The number of people booked must be at least 1.")
        return spots
