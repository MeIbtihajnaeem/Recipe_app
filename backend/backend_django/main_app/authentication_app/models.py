from django.db import models

# Create your models here.

from django.db import models


from django.db import models

from django.contrib.auth.models import User


# Recipe Model
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instructions = models.TextField(blank=True, null=True)  # New field

    recipe = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

# Ingredients Model
class Ingredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE) 
    ingredient = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    
# Recipe Model
class RecipePublic(models.Model):
    instructions = models.TextField(blank=True, null=True)  # New field
    recipe = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    
class IngredientsPublic(models.Model):
    recipe = models.ForeignKey(RecipePublic, on_delete=models.CASCADE) 
    ingredient = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

