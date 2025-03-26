from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    occupation = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Occupation (Optional)'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'occupation']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = UserProfile.objects.create(User=user, Occupation=self.cleaned_data['occupation'])
            profile.save()
        return user

class MakePostForm(forms.Form):
    url = forms.URLField(widget=forms.URLInput(), required=False)
