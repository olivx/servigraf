from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as _login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.template.loader import render_to_string
from account.models import Profile
from account.forms import PasswordResetConfirm, PasswordResetForm, PasswordChange, EmailUsernameAuthenticationForm
from account.tokens import account_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, force_bytes, force_text
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm

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

def login(request):
    # import ipdb; ipdb.set_trace()
    form = EmailUsernameAuthenticationForm(request.POST or None)
    # form = AuthenticationForm(request.POST or None)
    if not request.user.is_authenticated():
        if request.method ==  'POST':
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        _login(request, user)
                        if (request.user.profile.type == Profile.CLIENT_USER):
                            if request.user.profile.company_group is None:
                                logout(request)
                                messages.error(request, 'Usuário cliente não tem empresa associada.')
                                return redirect(resolve_url('account:login'))

                            # enviar para paginas de clientes
                            messages.success(request,'seja bem vindo, <strong>{}</strong>'.format(user.profile.full_name.title()))
                            return redirect(resolve_url('cliente:ticket_list'))
                        else:
                            # enviar para pgina de usario da servigraf
                            messages.success(request,'seja bem vindo, <strong>{}</strong>'.format(user.profile.full_name.title()))
                            return redirect(resolve_url('home'))
                    else:
                        error = 'O usuario {0}/{1} encontra-se desativado.'.format(user.username, user.email)
                        form.add_error(None, error)
                else:
                    # messages.error(request, 'Não é possivel fazer o login')
                    error ='Por favor, entre com um usuário e senha corretos. \
                                     Note que ambos os campos diferenciam maiúsculas e minúsculas.'

                    form.add_error(None, error)
                    form.add_error('username', 'verifique o usuário e tente novamente')
                    form.add_error('password', 'verifique o password e tente novamente')
    
    return render(request,'login.html', {'form': form })
