# coding: utf-8
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
from .celery import app
from orders.models import Order
from django.core.mail import send_mail


@app.task
def MailCreatedOrder(order_id):
    """
    Отправка Email сообщения о  покупке
    """
    order = Order.objects.get(id=order_id)
    subject = 'Заказ c номером {} из онлайн магазина Медодежды DocSimvol'.format(order.id)
    msgtext = get_template('mail_order_detail.html').render({ 'order': order, })
    msg = EmailMultiAlternatives(subject, msgtext, settings.SERVER_EMAIL, (order.email, settings.ORDER_EMAIL))
    msg.attach_alternative(msgtext, "text/html")
    mail = msg.send()
    return mail

@app.task
def sender_mail(theme, text):
    # почтальон рейтингов и комментариев о товаре
    send_mail(theme, text, settings.SERVER_EMAIL, [settings.STUFF_EMAIL], fail_silently=False)