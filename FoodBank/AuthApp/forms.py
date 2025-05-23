from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Donor, Foodbank, Recipient

class DonorRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=20, required=False)
    location = forms.CharField(max_length=255)
    preferred_donor_type = forms.ChoiceField(choices=Donor.DONOR_TYPE_CHOICES)
    donation_preference = forms.ChoiceField(choices=Donor.DONATION_PREFERENCE_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',) # Corrected: UserCreationForm handles password fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'DONOR'
        if commit:
            user.save()
        Donor.objects.create(
            user=user,
            full_name=self.cleaned_data['full_name'],
            phone_number=self.cleaned_data.get('phone_number'),
            location=self.cleaned_data['location'],
            preferred_donor_type=self.cleaned_data['preferred_donor_type'],
            donation_preference=self.cleaned_data['donation_preference']
        )
        return user

class FoodbankRegistrationForm(UserCreationForm):
    foodbank_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=20)
    contact_person = forms.CharField(max_length=255)
    picture = forms.ImageField(required=False)
    accepts_subsistence_donations = forms.BooleanField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',) # Corrected: UserCreationForm handles password fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'FOODBANK'
        if commit:
            user.save()
        Foodbank.objects.create(
            user=user,
            foodbank_name=self.cleaned_data['foodbank_name'],
            phone_number=self.cleaned_data['phone_number'],
            contact_person=self.cleaned_data['contact_person'],
            picture=self.cleaned_data.get('picture'),
            accepts_subsistence_donations=self.cleaned_data['accepts_subsistence_donations']
        )
        return user

class RecipientRegistrationForm(UserCreationForm):
    full_name_or_organization = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=20)
    contact_person = forms.CharField(max_length=255)
    location = forms.CharField(max_length=255)
    category = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',) # Corrected: UserCreationForm handles password fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'RECIPIENT'
        if commit:
            user.save()
        Recipient.objects.create(
            user=user,
            full_name_or_organization=self.cleaned_data['full_name_or_organization'],
            phone_number=self.cleaned_data['phone_number'],
            contact_person=self.cleaned_data['contact_person'],
            location=self.cleaned_data['location'],
            category=self.cleaned_data['category']
            # donation_preference_status is managed by the system
        )
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # Set the label for the username field to "Email"
        self.fields['username'].label = "Email"
