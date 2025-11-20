from asyncio import TaskGroup
from os import name
from django.urls import path
from recipe.views import RecipeListAPIView , RecipeCreateAPIView ,RecipeDetailAPIView, TagListAPIView 
from .views import TagListAPIView , RecipeUpdateDeleteAPIView , IngredientListAPIView

urlpatterns = [
    path('recipe/', RecipeListAPIView.as_view(), name='recipe-list'),
    path('recipe/create/',RecipeCreateAPIView.as_view() ,name='recipe-create'),
    path('recipe/<id>/',RecipeDetailAPIView.as_view(),name='recipe-detail'),
    path('tags/' , TagListAPIView.as_view() , name='Tags-list'),
    path('recipes/<int:id>/', RecipeUpdateDeleteAPIView.as_view(), name='recipe-update-delete'),
    path('ingredients/' , IngredientListAPIView.as_view(),name='ingredient-list')
    
]
