from rest_framework import serializers
from core.models import Recipe, Tag
import logging

logger = logging.getLogger(__name__)
# Serializer for Tag model
class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


# Serializer for Recipe model
class RecipeSerializer(serializers.ModelSerializer):
    tags = TagListSerializer(many=True, required=False)
    price = serializers.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        model = Recipe
        fields = ['id', 'user', 'title', 'description', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        # Step 1: Extract tags
        tags_data = validated_data.pop('tags', [])
        print("DEBUG: Tags extracted from validated_data:", tags_data)
        logger.debug(f"Tags extracted: {tags_data}")

        # Step 2: Get user from context
        user = self.context['user'] if 'user' in self.context else None
        print("DEBUG: User from context:", user)
        logger.debug(f"User for recipe: {user}")

        if not user:
            raise serializers.ValidationError("User is required to create a recipe.")

        # Step 3: Create recipe
        print("DEBUG: Creating recipe with data:", validated_data)
        recipe = Recipe.objects.create(user=user, **validated_data)
        print("DEBUG: Recipe created with ID:", recipe.id)
        logger.debug(f"Recipe created: {recipe}")

        # Step 4: Handle tags
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                user=user,
                name=tag_data['name']
            )
            recipe.tags.add(tag)
            print(f"DEBUG: Tag '{tag.name}' {'created' if created else 'exists'}, added to recipe")
            logger.debug(f"Tag {tag.name} ({'new' if created else 'existing'}) added to recipe {recipe.id}")

        # Step 5: Return recipe
        return recipe


  
