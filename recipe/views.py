from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions , generics
from core.models import Recipe , Tag
from recipe.serializers import RecipeSerializer
from drf_yasg.utils import swagger_auto_schema
from .serializers import TagListSerializer

class RecipeListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=['Get The List Of All Recipes'],
        operation_description="List all recipes",
        responses={200: RecipeSerializer(many=True)}
    )

    def get(self, request):
        """
        List all recipes (all users).
        """
        recipes = Recipe.objects.all().order_by('-id')  
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
