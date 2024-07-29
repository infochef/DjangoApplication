from django import forms
from django.core import validators
from .models import User

class AboutForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    # def clean_botcatcher(self):
    #     botcatcher = self.cleaned_data['botcatcher']
    #     if len(botcatcher) > 0:
    #         raise forms.ValidationError("Gotcha!! Bot catcher is " + botcatcher)
    #     return botcatcher

class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
