from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from account.forms import PasswordResetConfirm, PasswordResetForm
from account.tokens import account_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, force_bytes, force_text
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

# Create your views here.
from servigraf import settings


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
    user_id =  urlsafe_base64_decode(force_text(uidb64))
    user =  get_object_or_404(get_user_model(), pk=user_id)

    if user is not None and account_token_generator.check_token(user, token):
        validlink = True
        form = PasswordResetConfirm(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                pass

            else:
                pass
    context = {
        'validlink': validlink,
        'form':form
    }
    return render(request, 'password_reset_confirm.html', context)
