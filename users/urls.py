from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from .views import profile
from . import views

app_name = 'users'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('register/', user_views.register, name="user-register"),
    path('profile/<str:username>/', user_views.profile, name='profile'),
    path('myprofile/', user_views.myprofile, name="user-profile"),


]