from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from hitcount.views import HitCountDetailView
from django.shortcuts import redirect
from django.contrib import messages
from .models import Rating


from . import models

class RecipeListView(ListView):
    model = models.Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'

    

class RecipeDetailView(HitCountDetailView):
    model = models.Recipe
    template_name = 'recipes/recipe_detail.html'  # Make sure to specify this
    count_hit = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Access through the first related HitCount object
        if self.object.hit_count_generic.exists():
            context['hit_count'] = self.object.hit_count_generic.first().hits
        else:
            context['hit_count'] = 0
        return context
    
    def get_user_rating(self):
        if self.request.user.is_authenticated:
            try:
                return self.object.ratings.get(user=self.request.user).stars
            except Rating.DoesNotExist:
                return None
        return None
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to rate recipes')
            return redirect('login')
        
        stars = request.POST.get('stars')
        if stars and stars.isdigit():
            stars = int(stars)
            if 1 <= stars <= 5:
                Rating.objects.update_or_create(
                    recipe=self.object,
                    user=request.user,
                    defaults={'stars': stars}
                )
                messages.success(request, 'Thanks for rating')
            else:
                messages.error(request, 'Rating must be between 1-5')
        else:
            messages.error(request, 'Invalid rating value')
            
        return redirect('recipes-detail', pk=self.object.pk)

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Recipe
    success_url = reverse_lazy('recipes-home')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = models.Recipe
    fields = ['title', 'description', 'image', 'time_to_cook', 'difficulty', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('recipes-detail', kwargs={'pk': self.object.pk})

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Recipe
    fields = ['title', 'description']

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class SearchResultsView(ListView):
    model = models.Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = models.Recipe.objects.filter(title__icontains=query)
        return object_list


# Create your views here.
def home(request):
    recipes = models.Recipe.objects.all()
    context = {
        'recipes': recipes
    }
    return render(request, 'recipes/home.html', context)

def about(request):
    return render(request, 'recipes/about.html', {'title': 'about page'})
