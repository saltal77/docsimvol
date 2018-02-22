# coding: utf-8
from django.contrib import admin
from .models import Category, Product, Tips, Size, \
    Color, Rating, Firm, GoodName, NewsBlock, ActionBlock, AboutUsBlock, DeliveryBlock, ContactsBlock


class GoodNameAdmin(admin.ModelAdmin):
    list_display = ['name' ]
    list_filter = ['name']

class FirmAdmin(admin.ModelAdmin):
    list_display = ['name' ]
    list_filter = ['name']

class RatingAdmin(admin.ModelAdmin):
    list_display = ['created', 'product', 'rating', 'author', 'flag']
    list_filter = ['product', 'created', 'rating']

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name',]
# Модель категории
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}
# Модель Размер
class SizeAdmin(admin.ModelAdmin):
    list_display = ['sz',]
# Модель Тип
class TipsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}
# Модель товара
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'size', 'tips', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'name', 'size', 'tips', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name', )}

class NewsBlockAdmin(admin.ModelAdmin):
    list_display = ['title','created' ]
    list_filter = ['created']

class ActionBlockAdmin(admin.ModelAdmin):
    list_display = ['title','created' ]
    list_filter = ['created']

class AboutUsBlockAdmin(admin.ModelAdmin):
    list_display = ['slogan']

class DeliveryBlockAdmin(admin.ModelAdmin):
    list_display = ['slogan']

class ContactsBlockAdmin(admin.ModelAdmin):
    list_display = ['adress']


admin.site.register(GoodName, GoodNameAdmin)
admin.site.register(Firm, FirmAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Tips, TipsAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(NewsBlock, NewsBlockAdmin)
admin.site.register(ActionBlock, ActionBlockAdmin)
admin.site.register(AboutUsBlock, AboutUsBlockAdmin)
admin.site.register(DeliveryBlock, DeliveryBlockAdmin)
admin.site.register(ContactsBlock, ContactsBlockAdmin)
