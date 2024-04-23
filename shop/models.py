from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=150, db_index=True, verbose_name='Наименование')
    slug = models.CharField(max_length=150, db_index=True, unique=True, default=uuid.uuid4, verbose_name='Ссылка')
    image = models.ImageField(upload_to=' shop/static/shop/img/product/%Y/%m/%d', blank=True)
    description = models.TextField(max_length=1000, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цeнa')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    created = models.DateTimeField(default=timezone.now, verbose_name='Добавлен')
    uploaded = models.DateTimeField(auto_now=True, verbose_name='Изменен')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'), )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

