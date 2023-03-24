from django.shortcuts import render, redirect, get_object_or_404


from .forms import RegistrationForm,UserForm,UserProfileForm
from .models import Account, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


#varification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from store.models import Product
from orders.models import Order, OrderProduct

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) #gives default forms you can print template
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request,'Registration Successful')

            # user activitation, throgh mail link
            current_site = get_current_site(request)
            mail_subject = 'Please Activate your Account'
            message = render_to_string('accounts/account_varification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),

            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # return HttpResponse(message)
            messages.success(request, 'Registration Successful!')
            return redirect('/accounts/login?command=verification&email='+email)

    else:
        form = RegistrationForm()

    context = {
        'form': form,
        }
    return render(request,'accounts/register.html',context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')


    return render(request, 'accounts/login.html')




@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "you are loged out")
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulation your account is activated.')
        return redirect('login')
    else:
        messages.error(request,'Invilid link!')
        return redirect('register')





def forgetPassword(request):

    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #Reset Password
            current_site = get_current_site(request)
            mail_subject = 'Please Reset your Password'
            message = render_to_string('accounts/reset_email_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),

            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request,'Password reset email has been sent to your email.')
            return redirect('login')
        else:
            messages.error(request,'Account doesnot exist.')
            return redirect('forgetPassword')

    return render(request, 'accounts/forgetPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'this link has been expired')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user= Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset Successful')
            return redirect('login')
        else:
            messages.error(request,'Password do not Match!')
            return redirect('reset password')
    else:
        return render(request,'accounts/resetPassword.html')



@login_required(login_url = 'login')
def dashboard(request):
    new_product = Product.objects.filter(labels='new')[:3]

    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    userprofile = UserProfile.objects.get(user_id=request.user.id)

    context = {
        'new_product': new_product,
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url = 'login')
def my_order(request):
    orders = Order.objects.filter(user_id=request.user.id, is_ordered=True)
    # orderproduct = OrderProduct.objects.filter(order_id=request.user.id, ordered=True)
    context = {
        'orders':orders,
        # 'orderproduct':orderproduct,
    }

    return render(request, 'accounts/my_order.html', context)


@login_required(login_url = 'login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'userprofile': userprofile,
        }
    return render(request, 'accounts/edit_profile.html', context)

    return render(request, 'accounts/edit_profile.html')


@login_required(login_url = 'login')
def change_password_dashboard(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()

                messages.success(request, "Password updated Successfully.")
                return redirect('change_password_dash')
            else:
                messages.error(request, 'please enter valid current password')
                return redirect('change_password_dash')
        else:
            messages.error(request,'Password doesnot match !')
            return redirect('change_password_dash')

    return render(request, 'accounts/change_password_dashboard.html')