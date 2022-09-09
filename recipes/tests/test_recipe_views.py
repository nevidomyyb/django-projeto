from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeVIEWsTests(RecipeTestBase):
    # Home
    def tearDown(self) -> None:
        return super().tearDown()

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_templat(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipe_found_if_no_recipe(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn("<h1 align='center'>Sem receitas encontradas</h1>",
                      response.content.decode('utf-8'))

    def test_recipe__home_template_loads_recipe(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn('Recipe Title', content)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn("<h1 align='center'>Sem receitas encontradas</h1>",
                      response.content.decode('utf-8'))

    # Category

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipe_founds(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe__category_template_loads_recipe(self):
        needed_title = 'This is recipe title'
        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category',
                    kwargs={'category_id': recipe.category.id}))
        self.assertEqual(response.status_code, 404)

    # Detail

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipes)

    def test_recipe_detail_view_returns_404_if_no_recipe_founds(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe__recipe_template_loads_recipe(self):
        needed_title = 'This is a detailed page - It loads only one recipe'
        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe',
                    kwargs={'id': recipe.id}))
        self.assertEqual(response.status_code, 404)
