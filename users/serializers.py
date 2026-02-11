from users.models import CustomUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_pass = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name','email','phone', 'password', 'confirm_pass']


    def validate(self, attrs):
        password = attrs.get('password')
        confirm_pass = attrs.get('confirm_pass')

        if password != confirm_pass:
            raise ValidationError({'password': 'Parollar mos emas'})

        email = attrs.get('email')
        phone = attrs.get('phone')

        if not email and not phone:
            raise ValidationError(
                {'auth': 'Email yoki phone kiritilishi shart'}
            )

        if email and phone:
            raise ValidationError(
                {'auth': 'Faqat bittasini tanlang email yoki phone'}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_pass')
        user = CustomUser.objects.create_user(**validated_data)
#parolni heshlab saqlab qoyishga
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs['username'],
            password=attrs['password']
        )
#Basadagi malumot bilan mos kevotimi tekshiradi

        if not user:
            raise ValidationError("Username yoki parol xato")

        attrs['user'] = user
        return attrs

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=('username','first_name','email','phone')

class PhotoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=('photo',)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True,required=True)
    new_password=serializers.CharField(write_only=True,required=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise ValidationError('Eski parol xato')
        return old_password

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password']) #heshlashga
        user.save()
        return user

