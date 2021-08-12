from django.urls import path
from rest_framework.authtoken import views
from .views import ApiCall, RegisterView, AutomateUserCreation

urlpatterns = [
    path('', ApiCall.as_view()),
    path('get-few-user/<int:user_no>', ApiCall.as_view()),
    path('register', RegisterView.as_view()),
    path('auto-create', AutomateUserCreation.as_view()),
    path('auto_create/<int:users_no>', AutomateUserCreation.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
]