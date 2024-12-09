from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings



def send_confirmation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    confirmation_link = request.build_absolute_uri(
        reverse('confirm_email', kwargs={'uid': uid, 'token': token})
    )
    subject = "Подтверждение регистрации"
    message = f"Для подтверждения регистрации перейдите по ссылке: {confirmation_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])