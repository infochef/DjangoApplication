from django.shortcuts import render
from firstapp.models import *
from . import forms
from .forms import NewUserForm

# Create your views here.
def index(request):
    webpage = AccessRecord.objects.order_by('date')
    data_dict = {'webpage': webpage}
    # my_dict = {'insert_me':"Hello!!! I am coming from firstapp templates dir view.py"}
    return render(request, 'firstapp/index.html', context=data_dict)


def about(request):
    check = forms.AboutForm()

    if request.method == 'POST':
        check = forms.AboutForm(request.POST)

        if check.is_valid():
            print('VALIDATION SUCCESS')
            print('NAME:' + check.cleaned_data['name'])
            print('EMAIL:' + check.cleaned_data['email'])
            print('TEXT:' + check.cleaned_data['text'])

    return render(request, 'firstapp/formpage.html', {'check': check})

def users(request):
    form = NewUserForm()

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print('ERROR FORM INVALID')

    return render(request,'firstapp/SignUp.html',{'form':form})
