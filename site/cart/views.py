# coding: utf-8
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CartAddProductFormAuto
from cupons.forms import CuponApllyForm
from cupons.models import Cupon


@require_POST
def CartAdd(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                                  update_quantity=cd['update'])
    return redirect('cart:CartDetail')

def CartRemove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:CartDetail')


def CartDetail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductFormAuto(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                        })
    cupon_apply_form = CuponApllyForm()
    has_cupons = Cupon.objects.filter(active=True).count()
    return render(request, 'cart.html',
{'cart': cart, 'cupon_apply_form': cupon_apply_form, 'has_cupons': has_cupons})
