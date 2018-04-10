# coding: utf-8
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from .models import Category, Product, Rating, NewsBlock, ActionBlock, AboutUsBlock, DeliveryBlock, ContactsBlock
from cart.forms import CartAddProductForm
from django.db.models import Q, Avg, Sum, Max, Min, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage, EmptyPage
from .forms import RatingCreateForm, MailCreateForm, MyFilterForm
from myshop.tasks import *
from .decorators import check_recaptcha

def search(query, category=None):
    # обработка поиска
    q = str(query).strip()
    q1 = q.lower()
    q2 = q.title()
    if not category:
        return Product.objects.filter(Q(description__icontains=q1, available=True) |
                               Q(description__icontains=q2, available=True) |
                               Q(name__name__icontains=q1, available=True) |
                               Q(name__name__icontains=q2, available=True) |
                               Q(color__name__icontains=q1, available=True) |
                               Q(color__name__icontains=q2, available=True) |
                               Q(firm__name__icontains=q, available=True) |
                               Q(firm__name__icontains=q1, available=True) |
                               Q(firm__name__icontains=q2, available=True)).order_by('-created')
    else:
        return Product.objects.filter(Q(description__icontains=q1, category=category, available=True)|
                                   Q(description__icontains=q2, category=category, available=True)|
                                   Q(name__name__icontains=q1, category=category, available=True)|
                                   Q(name__name__icontains=q2, category=category, available=True)|
                                   Q(color__name__icontains=q1, category=category, available=True)|
                                   Q(color__name__icontains=q2, category=category, available=True)|
                                   Q(firm__name__icontains=q, category=category, available=True)|
                                   Q(firm__name__icontains=q1, category=category, available=True)|
                                   Q(firm__name__icontains=q2, category=category, available=True)).order_by('-created')

# автокомплит слов для jquery
def wordslistAutocomplete(prod):
    w = []
    for k in list(prod.values('name__name', 'color__name', 'firm__name')):
        if '-' in k['name__name'].lower():
            for i in k['name__name'].lower().split('-'):
                if i not in w:
                    w.append(i)
        else:
            if k['name__name'].lower() not in w:
                w.append(k['name__name'].lower())
        if k['color__name'].lower() not in w:
            w.append(k['color__name'].lower())
        for i in k['firm__name'].split():
            if i not in w:
                w.append(i)
    words = list(set(w))
    return words

# Пагинатор страниц
def pager(prod, pages, request):
    paginator = Paginator(prod, pages)
    page = request.GET.get('page')
    try:
        prod = paginator.page(page)
    except PageNotAnInteger:
        prod = paginator.page(1)
    except EmptyPage:
        prod = paginator.page(paginator.num_pages)
    return prod


def MainView(request):
    query = request.GET.get('query')
    products = Product.objects.filter(available=True).order_by('-created')
    bestseller = products.filter(available=True, order_items__gt=1).annotate(sells=Count('order_items')).order_by(
        '-sells')[:6]
    recommended = products.filter(available=True, recommended=True).order_by('-created')[:6]
    novosti = NewsBlock.objects.all().order_by('-created')
    if len(novosti) >= 2:
        novosti = novosti[:2]
    actions = ActionBlock.objects.all()
    if len(actions) >= 3:
        action1, action2, action3 = actions[:3]
    else:
        action1, action2, action3 = ('', '', '')

    if query:
        products = search(query)
        return render(request, 'base_home.html', {'bestseller':bestseller, 'recommended':recommended,
                                                      'products': products, 'qflag': query, 'novosti': novosti})

    ### Выбираем id  только по одному имени каждого товара из новых для главной страницы  ###
    m = {}
    for n in list(products.values('name', 'id')):
        if n['name'] not in m:
            m[n['name']] = n['id']
    products = products.filter(id__in=list(m.values()))[:8]
    return render(request, 'base_home.html', {'products':products, 'action1': action1, 'action2': action2,'action3': action3,
                'bestseller':bestseller, 'recommended':recommended, 'novosti': novosti})


def AboutView(request):
    text = AboutUsBlock.objects.all()
    return render(request, 'about-us.html', {'text': text})


def NewsView(request):
    novosti = NewsBlock.objects.all().order_by('-created')[:20]
    novosti = pager(novosti, 3, request)
    return render(request, 'news.html', {'novosti': novosti})

def NewsViewDetail(request, id):
    novost = get_object_or_404(NewsBlock, id=id)
    return render(request, 'newsdetail.html', {'novost': novost})

@check_recaptcha
def ContactsView(request):
    text = ContactsBlock.objects.all()
    mailing_form = MailCreateForm()
    if request.method == "POST":
        mailing_form = MailCreateForm(request.POST)
        if mailing_form.is_valid() and not request.POST['honey'] and request.recaptcha_is_valid:
            cd = mailing_form.cleaned_data
            tel = cd['tlf'] if cd['tlf'] else 'Не оставлено'
            text = '\n от: %s.\n e-mail: %s\n тел: %s\n Сообщение: %s.\n' \
                 % (cd['author'].title(), cd['email'], tel, cd['message'].capitalize())
            sender_mail.delay('Оставлено сообщение на сайте онлайн магазина DocSimvol', text)
            return render(request, 'messagecreated.html', {'author': cd['author']})

    return render(request, 'contact-us.html', {'mailing_form': mailing_form, 'text': text})


def DeliveryView(request):
    text = DeliveryBlock.objects.all()
    return render(request, 'delivery.html', {'text': text})


def ProductList(request):
    category = None
    categories = Category.objects.all()
    all_products = Product.objects.all()
    actions = ActionBlock.objects.all()
    query = request.GET.get('query')
    form = MyFilterForm(request.POST or request.GET or None)
    if request.method == "GET":
        if form.is_valid():
            cleandata = form.cleaned_data
            st_select = cleandata.get('t')
            sp_select = cleandata.get('p')
            price_min = cleandata.get('p_min')
            price_max = cleandata.get('p_max')
            sc_select = cleandata.get('c')
            if st_select or sp_select or price_max or price_min or sc_select:
                products = all_products.filter(available=True)
                if st_select != ' ' and st_select:
                    products = products.filter(tips__name=st_select)
                if price_min or price_max:
                    if price_max and not price_min:
                        products = products.filter(price__lte=price_max).order_by('price')
                    if price_min and not price_max:
                        products = products.filter(price__gte=price_min).order_by('price')
                    if price_max and price_min:
                        if price_max == price_min:
                           products = products.filter(price=price_min)
                        else:
                            products = products.filter(price__gte=price_min, price__lte=price_max).order_by('price')
                if sp_select != ' ' and sp_select:
                    if sp_select == 'Дороже':
                        products = products.order_by('-price')
                    if sp_select == 'Дешевле':
                        products = products.order_by('price')
                if sc_select != ' ' and sc_select and sc_select != '':
                    products = products.filter(color__name=sc_select)

                filteredproducts = pager(products, 9, request)
                return render(request, 'shop-product.html', {'category': category, 'categories': categories, 'actions':actions,
                                            'products': filteredproducts, 'form': form, 'words': wordslistAutocomplete(products)})
    if query:
        # поиск
        products = search(query)
        queryproducts = pager(products, 9, request)
        return render(request, 'shop-product.html', {'category': category, 'categories': categories,
                        'products': queryproducts, 'qflag': query, 'form': form, 'words': wordslistAutocomplete(products)})

    products = all_products.filter(available=True).order_by('-created')
    ### Выбираем id  только по одному имени каждого товара из новых для главной страницы  ###
    m = {}
    for n in list(products.values('name', 'id')):
        if n['name'] not in m:
            m[n['name']] = n['id']
    products = products.filter(id__in=list(m.values()))[:9]

    return render(request, 'shop-product.html', {'category': category,'categories': categories, 'actions':actions,
    'products': products, 'form': form, 'words': wordslistAutocomplete(all_products)})


def ProductCatItemList(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    categories = Category.objects.all()
    actions = ActionBlock.objects.all()
    form = MyFilterForm(request.POST or request.GET or None)
    if request.method == "GET":
        if form.is_valid():
            cleandata = form.cleaned_data
            st_select = cleandata.get('t')
            sp_select = cleandata.get('p')
            price_min = cleandata.get('p_min')
            price_max = cleandata.get('p_max')
            sc_select = cleandata.get('c')
            if st_select or sp_select or price_max or price_min or sc_select:
                products = Product.objects.filter(available=True, category=category)
                if st_select != ' ' and st_select:
                    products = products.filter(tips__name=st_select)
                if price_min or price_max:
                    if price_max and not price_min:
                        products = products.filter(price__lte=price_max).order_by('price')
                    if price_min and not price_max:
                        products = products.filter(price__gte=price_min).order_by('price')
                    if price_max and price_min:
                        if price_max == price_min:
                           products = products.filter(price=price_min)
                        else:
                            products = products.filter(price__gte=price_min, price__lte=price_max).order_by('price')
                if sp_select != ' ' and sp_select:
                    if sp_select == 'Дороже':
                        products = products.order_by('-price')
                    if sp_select == 'Дешевле':
                        products = products.order_by('price')
                if sc_select != ' ' and sc_select:
                    products = products.filter(color__name=sc_select)

                filteredproducts = pager(products, 9, request)
                return render(request, 'shop-product-category.html', {'category': category, 'categories': categories, 'actions':actions,
                        'products': filteredproducts, 'form': form, 'words': wordslistAutocomplete(products)})

    query = request.GET.get('query')
    if query:
        # поиск
        products = search(query, category)
        queryproducts = pager(products, 9, request)
        return render(request, 'shop-product-category.html', {'category': category, 'categories': categories,
             'products': queryproducts,  'form': form, 'qflag': query, 'words': wordslistAutocomplete(products)})

    products = Product.objects.filter(available=True, category=category).order_by('name')
    return render(request, 'shop-product-category.html', {'category': category,'categories': categories, 'actions':actions,
    'products': products, 'form': form, 'words': wordslistAutocomplete(products)})


def ProductDetail(request, id, slug):
    rating_form = RatingCreateForm()
    cart_product_form = CartAddProductForm()
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    ## все цвета и размеры на станице товара для данной модели ##
    clrs = []
    sizs = []
    for cs in list(Product.objects.filter(slug=slug).values('size__sz', 'color__name')):
        if cs['color__name'] not in clrs:
            clrs.append(cs['color__name'])
        if cs['size__sz'] not in sizs:
            sizs.append(cs['size__sz'])
    clrs = (', ').join(clrs)
    sizs = (', ').join(sizs)
    ######
    if request.method == "POST":
        rating_form = RatingCreateForm(request.POST)
        if rating_form.is_valid():
            cd = rating_form.cleaned_data
            Rating.objects.create(rating=cd['rating'], product_id=product.id, email=cd['email'],
                                  author=cd['author'], ratingcomment=cd['ratingcomment'])
            link = 'http://www.docsimvol.ru' + product.get_absolute_url()
            text = 'от: %s. \ne-mail: %s. \nОтзыв: %s. \nПоставил(а) оценку: %s. \nссылка на товар: %s \nНапоминание: необходимо разрешить показывать' \
                   ' этот отзыв на сайте или удалить...' % (
                   cd['author'].title(), cd['email'], cd['ratingcomment'].capitalize(), cd['rating'], link)
            sender_mail.delay('Оставлен новый комментарий о товаре', text)
            return render(request, 'ratecreated.html', {'author': cd['author']})

    return render(request, 'product-detail.html', {'categories': categories,
    'product': product,  'cart_product_form': cart_product_form, 'clrs':clrs, 'sizs':sizs, 'rating_form': rating_form})
