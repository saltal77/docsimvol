
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from shop.views import ContactsView, AboutView, NewsView, DeliveryView, NewsViewDetail

urlpatterns = [
    url(r'^adminka/', admin.site.urls),
    url(r'^about/', AboutView, name='AboutView'),
    url(r'^news/', NewsView, name='NewsView'),
    url(r'^newsdetails/(?P<id>\d+)/$', NewsViewDetail, name='NewsViewDetail'),
    url(r'^contacts/', ContactsView, name='ContactsView'),
    url(r'^delivery/', DeliveryView, name='DeliveryView'),
    url(r'^cupons/', include('cupons.urls', namespace='cupon')),
    url(r'^', include('shop.urls', namespace='shop')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^order/', include('orders.urls', namespace='orders')),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: \nHost: http://docsimvol.ru", content_type="text/plain")),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
