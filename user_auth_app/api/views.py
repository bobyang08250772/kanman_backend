from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User


class RegistrationView(APIView):
    """Handle user registration and return auth token."""

    def post(self, request):
        """Register a new user and return token + user info."""
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_user = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_user)
            data = {
                'user_id': saved_user.id, 
                'token': token.key,
                'fullname': f'{saved_user.first_name} {saved_user.last_name}',
                'email': saved_user.email
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):
    """Custom login view using email instead of username."""

    def post(self, request):
        """Authenticate user and return auth token."""
        data = request.data.copy()
        data['username'] = data.get('email', '')
        serializer = self.serializer_class(data=data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'fullname': f'{user.first_name} {user.last_name}',
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailCheckView(APIView):
    """Check if a user exists by email and return basic info."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return user info for a given email if it exists."""
        email = request.query_params.get('email', None)

        if email is None:
            return Response(
                {"error": "Email parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email=email)
            return Response({
                'id': user.id,
                'email': user.email,
                'fullname': f'{user.first_name} {user.last_name}',
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_400_BAD_REQUEST
            )
