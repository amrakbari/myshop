from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from config.django.base import APP_DOMAIN
from .models import BaseUser, Profile


def create_profile(*, user: BaseUser) -> Profile:
    return Profile.objects.create(user=user)


def create_user(*, email: str, password: str) -> BaseUser:
    return BaseUser.objects.create_user(email=email, password=password)


def send_activation_email(user: BaseUser):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = APP_DOMAIN + reverse('api:users:activate', args=[uid, token])
    subject = 'Activate your account'
    message = render_to_string('registration_activation_email.html', {'activation_link': activation_link})
    send_mail(subject, message, 'your_email@gmail.com', [user.email])


@transaction.atomic
def register(*, email: str, password: str) -> BaseUser:
    user = create_user(email=email, password=password)
    create_profile(user=user)
    send_activation_email(user)
    return user
