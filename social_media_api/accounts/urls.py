# accounts/urls.py
from django.urls import path
from .views import UserRegistrationView, CustomAuthToken, UserProfileView
from .views import Follow_User, Unfollow_User, UserRegistrationAPIView, CustomAuthTokenAPI
from .views import LogoutView, UserProfileAPIView, Follow_User_API

urlpatterns = [
    # URL for user registration (HTML form)
    path('register/', UserRegistrationView.as_view(), name='user-registration'),

    # URL for API registration
    path('api/register/', UserRegistrationAPIView.as_view(), name='api-user-registration'),

    # URL for login (HTML form)
    path('login/', CustomAuthToken.as_view(), name='token-login'),

    # URL for logout
    path('logout/', LogoutView.as_view(), name='logout'),

    # URL for API login
    path('api/login/', CustomAuthTokenAPI.as_view(), name='api-token-login'),

    # URL for user profile (HTML)
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    # URL for API profile
    path('api/profile/', UserProfileAPIView.as_view(), name='api-user-profile'),

    # URL for following a user (HTML)
    path('follow/<int:pk>/', Follow_User.as_view(), name='follow-user'),

    # URL for unfollowing a user (HTML)
    path('unfollow/<int:pk>/', Unfollow_User.as_view(), name='unfollow-user'),

    # URL for API follow/unfollow
    path('api/follow/<int:pk>/', Follow_User_API.as_view(), name='api-follow-user'),
]

["unfollow/<int:user_id>/", "follow/<int:user_id>"]