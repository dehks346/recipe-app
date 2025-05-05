from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg




# Create your models here.
class Recipe(models.Model, HitCountMixin):
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'
    DIFFICULTIES_CHOICES = {
        EASY: 'Easy',
        MEDIUM: 'Medium',
        HARD: 'HARD',
    }
    HEALTHY = 'Healthy'
    GLUTEN_FREE = 'Gluten Free'
    TAG_CHOICES = {
        HEALTHY: 'Healthy',
        GLUTEN_FREE: 'Gluten Free'
    }
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    
    time_to_cook = models.IntegerField(null=True, blank=True, default=0)
    difficulty = models.CharField(max_length=6, choices=DIFFICULTIES_CHOICES, default=EASY)
    tag = models.CharField(max_length=11, choices=TAG_CHOICES, null=True, blank=True)
    
    serves = models.IntegerField(default=1)
    calories = models.IntegerField(null=True, blank=True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    hit_count_generic = GenericRelation(
        'hitcount.HitCount',
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )    
    
    @property
    def average_rating(self):
        from django.db.models import Avg
        return self.ratings.aggregate(Avg('stars'))['stars__avg'] or 0
    
    @property
    def rating_count(self):
        return self.ratings.count()
    
    def get_absolute_url(self):
        return reverse("recipe-detail", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return self.title
    
class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('recipe', 'user')
