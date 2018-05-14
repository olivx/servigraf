from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from account.forms import PasswordResetConfirm, PasswordResetForm, PasswordChange
from account.tokens import account_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, force_bytes, force_text
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

# Create your views here.
from servigraf import settings


def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')


def reset_password(request):
    form = PasswordResetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            context = {}
            try:
                user = get_user_model().objects.get(email=form.cleaned_data['email'])
                context['token'] = account_token_generator.make_token(user)
                context['domain'] = get_current_site(request).domain
                context['user'] = user
                context['uid'] = urlsafe_base64_encode(force_bytes(user.pk))

                subject = 'Novo password para Servigraf Sistemas'
                message = render_to_string('password_reset_email.html', context, request=request)
                send_mail(subject=subject, message=message,
                          from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])

            except ObjectDoesNotExist:
                pass

            return render(request, 'password_reset_done.html')

    return render(request, 'password_reset_form.html', {'form': form})


def password_confirm(request, uidb64, token):
    user_id = urlsafe_base64_decode(force_text(uidb64))
    user = get_object_or_404(get_user_model(), pk=user_id)

    validlink = False
    if user is not None and account_token_generator.check_token(user, token):
        validlink = True
        form = PasswordResetConfirm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                password = form.cleaned_data['new_password1']
                user.set_password(password)
                user.save()

                return redirect('account:reset_password_complete')

    context = {
        'validlink': validlink,
        'form': form
    }
    return render(request, 'password_reset_confirm.html', context)


@login_required
def change_password(request):
    form = PasswordChange(request.POST or None, user=request.user)
    if request.POST:
        if form.is_valid():
            user = request.user
            password = form.cleaned_data['new_password2']
            user.set_password(password)
            user.save()

            current_user = authenticate(username=user.username, password=password)
            login(request, current_user)
            return render(request, 'password_change_done.html')

    context = {
        'form': form
    }
    return render(request, 'password_change_form.html', context)


def login(request, template_name='registration/login.html', authentication_form=AuthenticationForm):

    if request.is_authenticadated():
        return HttResponseRedirect(reverse('core:home'))

    form = AuthenticationForm(requestt.POST or None)
    if request.method ==  'POST':
        if form.is_valid():
            usernmane =  form.cleaned_data['username']
            password =  form.cleaned_data['password']

            user  = authenticate(usernmane, password)
            if user is not None and user.is_active:
                login(request, user')

                if user.profile.type ==  Profile.ESCOLA_DA_VILLA_USER:
                    return render(request, template_name='villa/home.html')
            else:
                messages.error(request, ('Usuário está desativado entre em contato com com a servigraf.'))

                return render(request, template_name=template_name, {'form': form })
