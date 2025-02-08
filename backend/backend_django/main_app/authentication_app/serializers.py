from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Recipe,Ingredients, RecipePublic,IngredientsPublic
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password', 'email']
        
        

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
        
class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['id', 'ingredient']
        
class RecipeWithIngredientsSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True, source='ingredients_set')  

    class Meta:
        model = Recipe
        fields = ['id', 'recipe', 'instructions','ingredients']
        
class PublicRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipePublic
        fields = '__all__'
        
class PublicIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientsPublic
        fields = ['id', 'ingredient']
        

class PublicRecipeWithIngredientsSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True, source='ingredientspublic_set')  

    class Meta:
        model = RecipePublic
        fields = ['id', 'recipe', 'ingredients', 'instructions']
