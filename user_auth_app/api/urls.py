from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegistrationView, CustomLoginView, EmailCheckView

urlpatterns = [
    path('api/registration/', RegistrationView.as_view(), name='registration'),
    path('api/login/', CustomLoginView.as_view(), name='login'),
    path('api/email-check/', EmailCheckView.as_view(), name='login')
]
