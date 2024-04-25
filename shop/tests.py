# Create your tests here.
# class TestShop(TestCase):
#     def test_index(self):
#         responce = self.client.get('')
#         self.assertEqual(responce.status_code,200)
from django.test import TestCase
from shop.models import Category, Product
from django.urls import reverse, resolve
from .views import product_list, product_detail

class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем объект категории для использования в тестах
        Category.objects.create(name='Тестовая категория', slug='test-category')



class TestUrls(TestCase):

    def test_product_list_url_resolves(self):
        url = reverse('shop:product_list')
        self.assertEqual(resolve(url).func, product_list)

    def test_product_detail_url_resolves(self):
        product = Product.objects.create(category=Category.objects.create(name='Тестовая категория', slug='test-category'), name='Тестовый продукт', slug='test-product', price=10.00)
        url = reverse('shop:product_detail', args=[product.id, product.slug])
        self.assertEqual(resolve(url).func, product_detail)

class ProductModelTest(TestCase):

    def test_name_label(self):
        product = Product.objects.create(category=Category.objects.create(name='Тестовая категория', slug='test-category'), name='Тестовый продукт', slug='test-product', price=10.00)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Наименование')

    def test_slug_label(self):
        product = Product.objects.create(category=Category.objects.create(name='Тестовая категория', slug='test-category'), name='Тестовый продукт', slug='test-product', price=10.00)
        field_label = product._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'Ссылка')

    def test_object_name_is_name(self):
        product = Product.objects.create(category=Category.objects.create(name='Тестовая категория', slug='test-category'), name='Тестовый продукт', slug='test-product', price=10.00)
        expected_object_name = product.name
        self.assertEqual(expected_object_name, str(product))