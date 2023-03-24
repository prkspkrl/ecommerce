from django.contrib import messages
from django.shortcuts import render
from .models import Contact
from .forms import FeedbackForm
from .models import Feedback

# Create your views here.

def contact(request):
    contact = Contact.objects.all()
    context= {
        'contact':contact,
    }
    return render(request, 'contact/contact.html',context)

def contact_message(request):
    if request.method =='POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        user = Feedback.objects.create(name=name, email=email, message=message)
        user.save()
        messages.success(request, 'Registeration Successful!')
        return render(request,'contact/contact.html')






