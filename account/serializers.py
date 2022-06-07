from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = get_user_model()


class RegisterApiSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs.get('password') != password2:
            raise serializers.ValidationError('Passwords did not match!')

        if not attrs.get('password').isalnum():
            raise serializers.ValidationError('Password field must be contain alpha and nums!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.pop('email')
        password = attrs.pop('password')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        else:
            raise serializers.ValidationError('Invalid password!')
        return attrs


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=30, required=True)
    code = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(min_length=4, required=True)
    password2 = serializers.CharField(min_length=4, required=True)

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords does not match')

        email = attrs['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exists')

        code = attrs['code']
        if user.activation_code != code:
            raise serializers.ValidationError('Code is incorrect')

        attrs['user'] = user

        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        user = data['user']

        user.set_password(data['password'])
        user.activation_code = ''
        user.save()

        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100 ,required=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {'bad_token': _('Token is invalid or expired!')}

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
