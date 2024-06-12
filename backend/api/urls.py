from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CustomUserViewSet, GetRecipeShortLink,
                       IngredientViewSet, RecipeViewSet, TagViewSet)

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet)
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('recipes/<int:recipe_id>/get-link/',
         GetRecipeShortLink.as_view(), name='get-link'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
