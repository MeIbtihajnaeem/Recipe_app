from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Recipe, Ingredients,RecipePublic,IngredientsPublic
from .serializers import IngredientsSerializer,RecipeSerializer,RecipeWithIngredientsSerializer,PublicRecipeSerializer,PublicRecipeWithIngredientsSerializer,PublicIngredientsSerializer
from django.db import transaction
from .serializers import UserSerializer
# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
    
#     def post(self,request,*args,**kwargs):
#         serializer = self.get_serializer(data = request.data)
#         serializer.is_valid(raise_exception = True)
#         user = serializer.save()
#         return Response({
#             "user": UserSerializer(user,context = self.get_serializer_context()).data,
#             "token": AuthToken.objects.create(user)[1]
#         })
    # def register_user(request):
    #     if request.method == 'POST':
    #         serializer = UserSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def create_recipe(request):
#     return Response("passed!")




@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getRecipe(request):
    user = request.user
    # recipes = Recipe.objects.prefetch_related('ingredients_set')
    recipes = Recipe.objects.filter(user=user).prefetch_related('ingredients_set')  # Filter by user

    serializer = RecipeWithIngredientsSerializer(recipes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_recipe(request):
    
    try:
        with transaction.atomic():
            user = request.user 
            recipe_data = request.data.get("recipe")
            instructions = request.data.get("instructions")
            ingredients_data = request.data.get("ingredients", []) 
            # recipe_serializer = RecipeSerializer(data = {"recipe": recipe_data})
            recipe_serializer = RecipeSerializer(data={"recipe": recipe_data, "user": user.id,"instructions":instructions})

            if not recipe_serializer.is_valid():
                return Response(recipe_serializer.errors, status=400)
            if not isinstance(ingredients_data, list) or not ingredients_data:
                return Response({"error": "At least one ingredient is required."}, status=400)
            # recipe = recipe_serializer.save()
            recipe = recipe_serializer.save(user=user)
            ingredients_list = [{"recipe": recipe.id, "ingredient": ing} for ing in ingredients_data]
            ingredients_serializer = IngredientsSerializer(data=ingredients_list, many=True)
            if not ingredients_serializer.is_valid():
                return Response(ingredients_serializer.errors, status=400)
            Ingredients.objects.bulk_create([
                Ingredients(recipe=recipe, ingredient=ing["ingredient"])
                for ing in ingredients_serializer.validated_data
            ])
            return Response({
                "message": "Recipe added successfully!",
                "recipe": recipe_serializer.data,
                "ingredients": ingredients_serializer.data
            }, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)




@api_view(['GET'])
def getRecipe_public(request):
    recipes = RecipePublic.objects.prefetch_related('ingredientspublic_set')
    serializer = PublicRecipeWithIngredientsSerializer(recipes, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def create_recipe_public(request):
    
    try:
        with transaction.atomic():
            recipe_data = request.data.get("recipe")
            instructions = request.data.get("instructions")
            ingredients_data = request.data.get("ingredients", []) 
            recipe_serializer = PublicRecipeSerializer(data = {"recipe": recipe_data,"instructions":instructions})
            if not recipe_serializer.is_valid():
                return Response(recipe_serializer.errors, status=400)
            if not isinstance(ingredients_data, list) or not ingredients_data:
                return Response({"error": "At least one ingredient is required."}, status=400)
            recipe = recipe_serializer.save()
            ingredients_list = [{"recipe": recipe.id, "ingredient": ing} for ing in ingredients_data]
            ingredients_serializer = PublicIngredientsSerializer(data=ingredients_list, many=True)
            if not ingredients_serializer.is_valid():
                return Response(ingredients_serializer.errors, status=400)
            IngredientsPublic.objects.bulk_create([
                IngredientsPublic(recipe=recipe, ingredient=ing["ingredient"])
                for ing in ingredients_serializer.validated_data
            ])
            return Response({
                "message": "Recipe added successfully!",
                "recipe": recipe_serializer.data,
                "ingredients": ingredients_serializer.data
            }, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

