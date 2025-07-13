from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration with full name and password confirmation."""
    
    fullname = serializers.CharField(max_length=255)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Create user with parsed full name and hashed password."""
        validated_data.pop('repeated_password')
        password = validated_data.pop('password')
        fullname = validated_data.pop('fullname')
        first_name, last_name = self.split_name(fullname)
        email = validated_data['email']

        user = User(
            username=self.generate_username_from_email(email),
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        """Check if both passwords match."""
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data

    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def split_name(self, fullname):
        """Split full name into first and last name."""
        parts = fullname.strip().split()
        first = parts[0]
        last = " ".join(parts[1:]) if len(parts) > 1 else ""
        return first, last

    def generate_username_from_email(self, email):
        """Generate a unique username based on the email prefix."""
        base = email.split('@')[0]
        username = base
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f'{base}_{counter}'
            counter += 1
        return username
