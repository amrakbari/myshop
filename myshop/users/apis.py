from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from django.core.validators import MinLengthValidator
from .validators import number_validator, special_char_validator, letter_validator
from myshop.users.models import BaseUser , Profile
from myshop.api.mixins import ApiAuthMixin
from myshop.users.selectors import get_profile
from myshop.users.services import register 
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from drf_spectacular.utils import extend_schema


class ProfileApi(ApiAuthMixin, APIView):

    class OutPutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile 
            fields = "__all__"

    @extend_schema(responses=OutPutSerializer)
    def get(self, request):
        query = get_profile(user=request.user)
        return Response(self.OutPutSerializer(query, context={"request":request}).data)


class RegisterApi(APIView):


    class InputRegisterSerializer(serializers.Serializer):
        email = serializers.EmailField(max_length=255)
        password = serializers.CharField(
                validators=[
                        number_validator,
                        letter_validator,
                        special_char_validator,
                        MinLengthValidator(limit_value=10)
                    ]
                )
        confirm_password = serializers.CharField(max_length=255)
        
        def validate_email(self, email):
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("email Already Taken")
            return email

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")
            
            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data


    class OutPutRegisterSerializer(serializers.ModelSerializer):

        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = BaseUser 
            fields = ("email", "token", "created_at", "updated_at")

        def get_token(self, user):
            data = dict()
            token_class = RefreshToken

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data


    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer)
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register(
                    email=serializer.validated_data.get("email"),
                    password=serializer.validated_data.get("password"),
                    )
        except Exception as ex:
            return Response(
                    str(ex),
                    status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(self.OutPutRegisterSerializer(user, context={"request":request}).data)


class ActivateApiView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = BaseUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, BaseUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'activation_successful.html')
        else:
            return render(request, 'activation_failed.html')
