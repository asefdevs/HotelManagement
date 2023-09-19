from rest_framework import serializers
from accounts.models import CustomUser
class UserSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=CustomUser
        fields=['username','email','password','password2']
        extra_kwargs={'password':{'write_only':True}}


    def create(self, validated_data):
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        username=self.validated_data['username']
        email=self.validated_data['email']
        if password!= password2:
            raise serializers.ValidationError({'password2':'passwords doesnt match'})
        user=CustomUser.objects.create(
            username=username,
            email=email,
            password=password
        )
        user.set_password(password)
        user.save()
        return user
    def validate_username(self,value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError({'username':'username already exists'})
        return value
    def validate_email(self,value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError({'email':'email already exists'})
        return value
    def validate_password(self,value):
        if len(value)<8:
            raise serializers.ValidationError({'password':'password must be at least 8 characters'})
        return value