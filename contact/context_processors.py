from .models import Socialmedia
from .models import Contact

def social_link(request):
    social_link = Socialmedia.objects.all()
    contact = Contact.objects.all()
    return dict(social_link=social_link,contact=contact)
