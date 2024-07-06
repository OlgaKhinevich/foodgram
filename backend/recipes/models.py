from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.urls import reverse

from users.models import User


class Tag(models.Model):
    """ Модель 'Тег' """

    name = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        verbose_name='Slug',
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Модель 'Ингредиент' """

    name = models.CharField(
        max_length=128,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=64,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """ Модель 'Рецепт' """

    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор публикации',
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        upload_to='recipe_images',
        verbose_name='Картинка рецепта',
    )
    text = models.TextField(
        verbose_name='Текстовое описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты для рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, message='Минимальное значение 1!')],
        verbose_name='Время приготовления рецепта в минутах',
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время публикации'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'pk': self.pk})


class IngredientInRecipe(models.Model):
    """ Модель количества нгредиента в рецепте """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(
            limit_value=0.01,
            message='Минимальное количество 1!'),
        ),
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'количество ингредиента'
        verbose_name_plural = 'Количество ингредиента'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'
            )
        ]

    def __str__(self):
        return (
            f'''{self.ingredient.name}
            ({self.ingredient.measurement_unit}) - {self.amount} '''
        )


class Favorite(models.Model):
    """ Модель 'Избранное' """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Избранное'


class ShoppingCart(models.Model):
    """ Модель 'Список покупок' """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Список покупок'


class ShortLink(models.Model):
    """ Модель 'Короткая ссылка' """

    original_url = models.URLField(
        max_length=256,
        verbose_name='Полная ссылка рецепта',
    )
    short_link = models.CharField(
        max_length=45,
        unique=True,
        verbose_name='Короткая ссылка рецепта',
    )

    class Meta:
        verbose_name = 'короткая ссылка'
        verbose_name_plural = 'Короткие ссылки'

    def __str__(self):
        return self.short_link
