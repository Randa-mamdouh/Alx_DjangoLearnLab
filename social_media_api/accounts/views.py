from django.shortcuts import render, redirect
from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions
from .models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import CustomUserRegistrationForm, CustomAuthenticationForm
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout




# HTML Form-based registration view
class UserRegistrationView(View):
    def get(self, request):
        form = CustomUserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Create token for the user
            token, _ = Token.objects.get_or_create(user=user)
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('token-login')
        return render(request, 'accounts/register.html', {'form': form})

# API-based registration view
class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# HTML Form-based login view
class CustomAuthToken(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Create or get token for API access
            token, _ = Token.objects.get_or_create(user=user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('user-profile')
        return render(request, 'accounts/login.html', {'form': form})

# API Token login view
class CustomAuthTokenAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

["generics.GenericAPIView", "permissions.IsAuthenticated", "CustomUser.objects.all()"]

# Create your views here.

class Follow_User(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to follow users.')
            return redirect('token-login')

        try:
            user_to_follow = CustomUser.objects.get(pk=pk)
            if user_to_follow != request.user:
                request.user.following.add(user_to_follow)
                messages.success(request, f'You are now following {user_to_follow.username}!')
            else:
                messages.error(request, 'You cannot follow yourself.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found.')

        return redirect('user-profile')

class Unfollow_User(View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to unfollow users.')
            return redirect('token-login')

        try:
            user_to_unfollow = CustomUser.objects.get(pk=pk)
            request.user.following.remove(user_to_unfollow)
            messages.success(request, f'You have unfollowed {user_to_unfollow.username}.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found.')

        return redirect('user-profile')

# API Follow/Unfollow Views
class Follow_User_API(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            user_to_follow = CustomUser.objects.get(pk=pk)
            request.user.following.add(user_to_follow)
            return Response({"message": f"You are now following {user_to_follow.username}"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            user_to_unfollow = CustomUser.objects.get(pk=pk)
            request.user.following.remove(user_to_unfollow)
            return Response({"message": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to view your profile.')
            return redirect('token-login')

        # Get all users for the "All Users" section
        all_users = CustomUser.objects.exclude(id=request.user.id)

        return render(request, 'accounts/profile.html', {
            'user': request.user,
            'all_users': all_users
        })

    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to update your profile.')
            return redirect('token-login')

        # Handle profile update
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.bio = request.POST.get('bio', user.bio)

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user-profile')

# API Profile View
class UserProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('token-login')
