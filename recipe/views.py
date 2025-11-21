from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions , generics
from core.models import Recipe , Tag , Ingredient
from recipe.serializers import RecipeSerializer
from drf_yasg.utils import swagger_auto_schema
from .serializers import TagListSerializer , IngredientSerializer
from drf_yasg import openapi

from drf_spectacular.utils import extend_schema, OpenApiParameter


class RecipeListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Get The List Of All Recipes'],
        operation_description="List all recipes. Use ?tags=1,2 to filter by tag IDs.",
        manual_parameters=[
            openapi.Parameter(
                'tags',
                openapi.IN_QUERY,
                description="Comma separated tag IDs for filtering (e.g: 1,2,3)",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: RecipeSerializer(many=True)}
    )
    
    def get(self, request):
        """
        List all recipes (all users) + filtering by tags.
        """
        recipes = Recipe.objects.all().order_by('-id')

        # --- filtering ---
        tag_ids = request.query_params.get("tags")
        if tag_ids:
            tag_ids = [int(tag) for tag in tag_ids.split(",")]
            recipes = recipes.filter(tags__id__in=tag_ids).distinct()

        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class RecipeCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Post Any Recipe'],
        operation_description="Create a new recipe",
        request_body=RecipeSerializer,
        responses={201: RecipeSerializer}
    )
    def post(self, request):
        """
        Create a new recipe. User will be set automatically.
        """
        serializer = RecipeSerializer(data=request.data , context={'user': request.user}  )
        if serializer.is_valid(raise_exception=True):
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['View Recipe Details'],
        operation_description="Get a single recipe by ID",
        responses={200: RecipeSerializer}
    )
    def get(self, request, id):
        """
        Retrieve a single recipe by its ID.
        """
        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return Response(
                {"error": "Recipe not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TagListAPIView(generics.ListAPIView):
    serializer_class = TagListSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Tags'],
        operation_description="List all tags of the logged-in user",
        responses={200: TagListSerializer(many=True)}
    )
    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).order_by('name')

        

class RecipeUpdateDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Update Recipe'],
        operation_description="Update recipe using PUT",
        request_body=RecipeSerializer,
        responses={200: RecipeSerializer}
    )
    def put(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id, user=request.user)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=404)

        serializer = RecipeSerializer(
            recipe,
            data=request.data,
            context={'user': request.user}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        tags=['Update Recipe'],
        operation_description="Update partial recipe using PATCH",
        request_body=RecipeSerializer,
        responses={200: RecipeSerializer}
    )
    def patch(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id, user=request.user)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=404)

        serializer = RecipeSerializer(
            recipe,
            data=request.data,
            partial=True,
            context={'user': request.user}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        tags=['Delete Recipe'],
        operation_description="Delete a recipe",
        responses={204: "No content"}
    )
    def delete(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id, user=request.user)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=404)

        recipe.delete()
        return Response(status=204)

class IngredientListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Get Ingredients List'],
        operation_description="Get all ingredients of the logged-in user",
        responses={200: IngredientSerializer(many=True)}
    )
    def get(self, request):
        """
        List all ingredients for the logged-in user.
        """
        ingredients = Ingredient.objects.filter(user=request.user).order_by('name')
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






