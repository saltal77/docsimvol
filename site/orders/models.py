# coding: utf-8
from django.db import models
from shop.models import Product
from cupons.models import Cupon
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    email = models.EmailField(verbose_name='Email')
    address = models.CharField(verbose_name='Адрес', max_length=250)
    tlf = models.CharField(verbose_name='Телефон', max_length=20)
    city = models.CharField(verbose_name='Город', max_length=100)
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлен', auto_now=True)
    paid = models.BooleanField(verbose_name='Оплачен', default=False)
    executed = models.BooleanField(verbose_name='Выполнен', default=False)
    cupon = models.ForeignKey(Cupon, verbose_name='Промокод', related_name='orders', null=True, blank=True)
    discount = models.IntegerField(verbose_name='Скидка', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    delivery = models.BooleanField(verbose_name='Доставка', default=False)
    comment = models.CharField(verbose_name='Комментарий', max_length=100, blank=True)


    class Meta:
        ordering = ('-created', )
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ: {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))

    def get_total_discount(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost * (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items', verbose_name='Товар')
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Предмет заказа'
        verbose_name_plural = 'Предметы заказа'