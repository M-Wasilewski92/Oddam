from django import forms


class DonationCreationForm(forms.Form):
    quantity = forms.IntegerField()
    address = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=15)
    city = forms.CharField(max_length=30)
    zip_code = forms.CharField(max_length=10)
    pick_up_date = forms.DateField(widget=forms.DateInput)
    pick_up_time = forms.TimeField()
    pick_up_comment = forms.CharField(widget=forms.Textarea)
    institution_id = forms.IntegerField()
    category_ids = forms.CharField(max_length=5)


class IsTakenForm(forms.Form):
    is_taken = forms.BooleanField(initial=True, required=False)


class ContactForm(forms.Form):
    first_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Imię"})
    )
    last_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Nazwisko"})
    )
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
