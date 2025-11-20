from rest_framework import serializers
from core.models import Recipe, Tag , Ingredient
import logging

logger = logging.getLogger(__name__)
# Serializer for Tag model
class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']

# Serializer for Recipe model
class RecipeSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(many=True, required=False)
    price = serializers.DecimalField(max_digits=7, decimal_places=2)
    ingredients=IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'user', 'title', 'description', 'time_minutes', 'price', 'link', 'tags' , 'ingredients']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        ingredients_data = validated_data.pop('ingredients', [])  # NEW

        user = self.context['user'] if 'user' in self.context else None
        if not user:
            raise serializers.ValidationError("User is required to create a recipe.")

        # Create the recipe
        recipe = Recipe.objects.create(user=user, **validated_data)

        # Handle tags
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(user=user, name=tag_data['name'])
            recipe.tags.add(tag)

        # Handle ingredients
        for ingredient_data in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(user=user, name=ingredient_data['name'])
            recipe.ingredients.add(ingredient)  # if you have ManyToManyField in Recipe for ingredients

        return recipe


    def update(self, instance, validated_data):
    # Extract tags if provided
     tags_data = validated_data.pop('tags', None)

    # Update normal fields
     for attr, value in validated_data.items():
        setattr(instance, attr, value)

     instance.save()

    # If tags provided → reset and update them
     if tags_data is not None:
        instance.tags.clear()
        user = self.context['user']

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                user=user,
                name=tag_data['name']
            )
            instance.tags.add(tag)

     return instance





  
