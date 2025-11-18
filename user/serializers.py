from rest_framework import serializers
from core.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password' , 'is_active', 'is_staff']

    def create(self, validated_data):
        # Use core UserManager's create_user method
        return User.objects.create_user(**validated_data)


    def update(self, instance, validated_data):
        # Update only name and email
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
        else:
            raise serializers.ValidationError('Both email and password are required.')
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        # Just return user
        return validated_data['user']

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': instance.id,
                'email': instance.email,
                'name': instance.name,
                'is_active': instance.is_active,
                'is_staff': instance.is_staff,
            }
        }
