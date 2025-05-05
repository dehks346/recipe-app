from django.urls import path
from . import views
from .views import SearchResultsView

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipes-home'),
    path('about/', views.about, name='recipes-about'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipes-detail'),
    path('recipe/create/', views.RecipeCreateView.as_view(), name='recipes-create'),
    path('recipe/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='recipes-update'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipes-delete'),
    path("search/", SearchResultsView.as_view(), name="search_results"),
]