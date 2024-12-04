from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

def send_confirmation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = user.pk
    domain = get_current_site(request).domain
    confirmation_link = request.build_absolute_uri(
        reverse('confirm_email', kwargs={'uid': uid, 'token': token})
    )
    subject = "Подтверждение регистрации"
    message = render_to_string('registration/confirmation_email.html', {
        'user': user,
        'confirmation_link': confirmation_link,
        'domain': domain,
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])