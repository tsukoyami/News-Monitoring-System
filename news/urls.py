# urls.py
from django.urls import path
from .views import signup, user_login, user_stories, logout, user_sources, add_source, edit_source, delete_source, add_story, delete_story, edit_story, update_stories, search_user_sources, search_user_stories

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', user_login, name='login'),
    path('logout/', logout, name='logout'),
    path('user-stories/', user_stories, name='user_stories'),
    path('add_story/', add_story, name='add_story'),
    path('edit_story/<int:pk>/', edit_story, name='edit_story'),
    path('delete_story/<int:pk>/', delete_story, name='delete_story'),
    path('user-sources/', user_sources, name='user_sources'),
    path('sources/add/', add_source, name='add_source'),
    path('edit/<int:pk>/', edit_source, name='edit_source'),
    path('delete/<int:pk>/', delete_source, name='delete_source'),
    path('update-stories/', update_stories, name='update_stories'),
    path('search-user-sources/', search_user_sources, name='search_user_sources'),
    path('search-user-stories/', search_user_stories, name='search_user_stories'),
    # Add other URL patterns as needed
]
