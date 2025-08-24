from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from django.contrib.auth.views import LoginView 
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .views import register_librarian, get_librarian_for_library
from .views import register
from .import views


from django.urls import path
from . import views



from django.urls import path
from . import views


urlpatterns = [ 
    path('login/', LoginView.as_view(template_name='')),
    path('logout/', LogoutView.as_view(template_name='')),
    path('Admin-dashboard/', views.Admin_only_view, name='Admin_dashboard'),
    path('register/', views.register.as_view(), name='register'),
    
    path('login/', loginview.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', logoutview.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    path('library/', LibraryDetailView.as_view(), name='library_detail'),
    path('list_books/', list_books, name='list_books'),
    
    path('admin/', views.admin.view, name='admin_view'),
    
    path('librarian/', views.librarian.view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/', views.add_book, name='edit_book'),
    #path('edit/<int:pk>/'),
    path('delete/<int:pk>/', views.delete_book, name='delete_book'),

]
