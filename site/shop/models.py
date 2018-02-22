# coding: utf-8
from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from datetime import timedelta, datetime

# Модель размер продукта
class Size(models.Model):
    PROD_SIZES = (
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('44', '44'),
        ('46', '46'),
        ('48', '48'),
        ('50', '50'),
        ('52', '52'),
        ('54', '54'),
        ('56', '56'),
        ('58', '58'),
        ('60', '60'),
        ('36/39', '36/39'),
        ('40/43', '40/43'),
        ('N', 'Нет')
    )
    sz = models.CharField(db_index=True, unique=True, max_length=5, choices=PROD_SIZES, verbose_name="Размер")

    class Meta:
        ordering = ['sz']
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.sz


# Модель Цвет
class Color(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="Цвет", unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.name


# Модель Производитель
class Firm(models.Model):
    name = models.CharField(max_length=200, db_index=True , verbose_name="Производитель", unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


# Модель категории
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def get_absolute_url(self):
        return reverse('shop:ProductListByCategory', args=[self.slug])

    def distinctgoods(self):
        # возвращает количество назаний товаров в категории
        return len(set(self.types.values_list('name')))

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


# Модель Тип продукта
class Tips(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="Тип")
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name


# Модель Название товара
class GoodName(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название", unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'

    def __str__(self):
        return self.name


# Модель продукта
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='types', verbose_name="Категория")
    tips = models.ForeignKey(Tips, related_name='products', verbose_name="Тип")
    size = models.ForeignKey(Size, related_name='sizes', verbose_name="Размер")
    color = models.ForeignKey(Color, related_name='colors', verbose_name="Цвет")
    firm = models.ForeignKey(Firm, related_name='firms', verbose_name="Производитель")
    name = models.ForeignKey(GoodName, related_name='goodnames', verbose_name="Название")
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name="Изображение товара 750x1000")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name="На складе")
    available = models.BooleanField(default=True, verbose_name="Доступен")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Занесен")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    recommended = models.BooleanField(default=False, verbose_name='Рекоммендуемый')

    def get_absolute_url(self):
        return reverse('shop:ProductDetail', args=[self.id, self.slug])

    def get_stock_status(self):
        return True if self.stock > 0 else False

    def str_category(self):
        return str(self.category)

    def str_id(self):
        # возвращает стоку с id товара
        return str(self.id)

    def has_size(self):
        # возвращает строковое представление размера для сравнения по условию в шаблоне  (тк поле внешнее и возвращается просто число)
        return str(self.size)

    def has_tips(self):
        # возвращает строковое представление Тип (М/Ж) для сравнения по условию в шаблоне (тк поле внешнее и возвращается просто число)
        return str(self.tips)

    def get_ratings(self):
        # собираем все рейтинги через связь related_name='rate' в таблице Rating из Product
        # собираем именно значения rating и переводим в список
        # выводим среднее арифметическое
        r = list(self.rate.filter(flag=True).values_list('rating'))
        c = len(r)
        m = 0
        for i in r:
            m += i[0]
        return round(m / c)

    def allow_comments(self):
        return self.rate.filter(flag=True).count()

    def is_recommend(self):
        return self.recommended

    def novelty(self):
        # возвращает true если товар заведен не позднее 14 дней назад
        days_left = timezone.now() - self.created
        return days_left < timedelta(days=14)

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return str(self.name)


# Модель Рейтинг
class Rating(models.Model):
    rating = models.PositiveIntegerField(verbose_name='Рейтинг', default=0)
    product = models.ForeignKey(Product, related_name='rate', verbose_name="Товар")
    author = models.CharField(max_length=50, db_index=True, verbose_name="Автор")
    email = models.EmailField(verbose_name='Почта', max_length=80)
    ratingcomment = models.TextField(verbose_name='Отзыв')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Оставлен")
    flag = models.BooleanField(verbose_name='Отобразить на сайте', default=False)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return str(self.rating)

    def display(self):
        return self.flag


# Модель Новости Магазина
class NewsBlock(models.Model):
    author = models.CharField(max_length=50, db_index=True, verbose_name="Автор", default="Администрация")
    title = models.CharField(max_length=80, verbose_name='Заголовок')
    news = models.TextField(verbose_name='Новость')
    image = models.ImageField(upload_to='news/%Y/%m/%d/', verbose_name="Фото новости 870x400")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        ordering = ['created']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('NewsViewDetail', args=[self.id])


# Модель О нас
class ActionBlock(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок Акции 50 символов')
    actiontext = models.CharField(max_length=60, verbose_name='Краткий текст Акции 60 символов')
    actionbigtext = models.CharField(max_length=200, verbose_name='Текст Акции 200 символов')
    btntext = models.CharField(max_length=25, verbose_name='Кнопка 25 символов')
    imageA = models.ImageField(upload_to='action/%Y/%m/%d/', verbose_name="Фото акции (мал. 570x296)")
    imageB = models.ImageField(upload_to='banner/%Y/%m/%d/', verbose_name="Баннер на Главной (бол. 1605x660)")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        ordering = ['created']
        verbose_name = 'Акция на Главной'
        verbose_name_plural = 'Акции на Главной'

    def __str__(self):
        return self.title

# Модель о Нас
class AboutUsBlock(models.Model):
    about = models.TextField(verbose_name='О нас')
    slogan = models.CharField(max_length=50, verbose_name='Слоган 50 символов')

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'

    def __str__(self):
        return self.slogan

# Модель о доставке
class DeliveryBlock(models.Model):
    deliver = models.TextField(verbose_name='О Доставке')
    slogan = models.CharField(max_length=50, verbose_name='Слоган 50 символов')

    class Meta:
        verbose_name = 'О Доставке'
        verbose_name_plural = 'О Доставке'

    def __str__(self):
        return self.slogan

# Модель Контакты
class ContactsBlock(models.Model):
    adress = models.TextField(verbose_name='Адрес')
    route = models.TextField(verbose_name='Описание маршрута')

    class Meta:
        verbose_name = 'Адрес и Маршрут'
        verbose_name_plural = 'Адрес и Маршрут'

    def __str__(self):
        return self.adress

