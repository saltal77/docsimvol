# coding: utf-8
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Order
from shop.models import DeliveryBlock
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from cupons.models import Cupon
from myshop.tasks import *


def OrderCreate(request):
    cart = Cart(request)
    text = DeliveryBlock.objects.all()
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.cupon:
                order.cupon = cart.cupon
                order.discount = cart.cupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            MailCreatedOrder.delay(order.id)
            return render(request, 'created.html', {'order': order})

    has_cupons = Cupon.objects.filter(active=True).count()
    form = OrderCreateForm(request.POST or None)
    return render(request, 'order_base.html', {'cart': cart,
                                       'form': form, 'has_cupons': has_cupons, 'text':text })

@staff_member_required
def AdminOrderDetail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin_order_detail.html', {'order': order})


@staff_member_required
def AdminOrderPDF(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
               stylesheets=[weasyprint.CSS('/home/someuseronsomeserver/web/site/static/css/bootstrap.min.css')])
    return response
