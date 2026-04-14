from django import forms

SERVICE_CHOICES = [
    ('', '— Select a service —'),
    ('Junk Removal', 'Junk Removal'),
    ('Residential Cleaning', 'Residential Cleaning'),
    ('Air BnB Cleaning', 'Air BnB Cleaning'),
    ('Move In/Move Out Cleaning', 'Move In/Move Out Cleaning'),
    ('Recurring Maid Services', 'Recurring Maid Services'),
    ('Fence Removal', 'Fence Removal'),
    ('Estate Clean-Out', 'Estate Clean-Out'),
    ('Eviction Clean-Out', 'Eviction Clean-Out'),
    ('Foreclosure Clean-Out', 'Foreclosure Clean-Out'),
    ('Bulk Cardboard Removal & Pickup', 'Bulk Cardboard Removal & Pickup'),
    ('Garage Clean-Out', 'Garage Clean-Out'),
    ('Storage Unit Clean-Out', 'Storage Unit Clean-Out'),
    ('Hot Tub Removal', 'Hot Tub Removal'),
    ('Other', 'Other'),
]

TIME_CHOICES = [
    ('', '— Preferred time —'),
    ('Morning (8am–12pm)', 'Morning (8am–12pm)'),
    ('Afternoon (12pm–5pm)', 'Afternoon (12pm–5pm)'),
    ('Anytime', 'Anytime'),
]


class QuoteForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='First Name')
    last_name = forms.CharField(max_length=100, label='Last Name')
    email = forms.EmailField(label='Email Address')
    phone = forms.CharField(max_length=20, label='Phone Number')
    service_type = forms.ChoiceField(choices=SERVICE_CHOICES, label='Service Needed')
    address = forms.CharField(max_length=255, label='Property Address', required=False)
    city = forms.CharField(max_length=100, label='City', required=False)
    state = forms.CharField(max_length=50, label='State', required=False, initial='TN')
    zip_code = forms.CharField(max_length=10, label='Zip Code', required=False)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Describe what you need removed or cleaned',
        required=False,
    )
    photo = forms.FileField(
        required=False,
        label='Upload a photo (optional)',
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
    )


class BookingForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='First Name')
    last_name = forms.CharField(max_length=100, label='Last Name')
    email = forms.EmailField(label='Email Address')
    phone = forms.CharField(max_length=20, label='Phone Number')
    service_type = forms.ChoiceField(choices=SERVICE_CHOICES, label='Service Needed')
    address = forms.CharField(max_length=255, label='Property Address')
    city = forms.CharField(max_length=100, label='City')
    state = forms.CharField(max_length=50, label='State', initial='TN')
    zip_code = forms.CharField(max_length=10, label='Zip Code')
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Preferred Date',
        required=False,
    )
    preferred_time = forms.ChoiceField(choices=TIME_CHOICES, label='Preferred Time Window', required=False)
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Additional Notes',
        required=False,
    )
