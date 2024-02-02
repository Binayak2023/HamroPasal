from django.shortcuts import render
from .models import Contact, PromoCode, SubscriptionEmail, Product, SlideContent, BannerContent
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.views.generic import View
from registration.forms import CustomerForm
from registration.models import Customer
from .models import MyCart, OrderPlaced
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import logging
import os
import datetime
# pylint: disable=no-member
# Create your views here.

def log_activity(message):
    log_data = f"{message} - {datetime.datetime.now()}\n"
    log_path = os.path.join(os.path.dirname(__file__), 'activity_log_home.txt')

    with open(log_path, 'a') as log_file:
        log_file.write(log_data)

# Create your views here.
def home(request):
    log_activity(f"User {request.user.username if request.user.is_authenticated else 'Anonymous'} visited the home page")

    disprod = Product.objects.all().order_by('?')[:8]
    allprod = Product.objects.all().order_by('-id')[:12]
    slides = SlideContent.objects.all().order_by('-id')[:5]
    banner = BannerContent.objects.all().order_by('-id')[:1][0]
    if request.user.is_authenticated:
        products = Product.objects.filter(users_wishlist=request.user)
        wishlistcount = products.count()
        cartprod = MyCart.objects.filter(user=request.user) 
        cartprodcount = cartprod.count()
    else:
        wishlistcount = ''
        cartprodcount = ''
    context = {
        'disprod':disprod,
        'allprod':allprod,
        'slides':slides,
        'banner':banner,
        'wishlistcount': wishlistcount,
        'cartprodcount': cartprodcount,
    }
    return render(request, 'home/index.html', context)

def productlist(request):
    log_activity(f"User {request.user.username if request.user.is_authenticated else 'Anonymous'} visited the product list page with sorting option {request.GET.get('sort', 1)}")

    sort = request.GET.get('sort', 1)
    sortint = int(sort)
    if sortint == 1:
        allprod = Product.objects.all().order_by('?')
    elif sortint == 2:
        allprod = Product.objects.all().order_by('selling_price')
    elif sortint == 3:
        allprod = Product.objects.all().order_by('-selling_price')
    else:
        allprod = Product.objects.all().order_by('?')
    paginator = Paginator(allprod, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    total_pages = page_obj.paginator.num_pages
    pages = []
    pp = int(page_number) - 2
    p = int(page_number) - 1
    pn = int(page_number)
    n = int(page_number) + 1
    nn = int(page_number) + 2
    set1 = {pp, p, pn, n, nn}
    for i in range(total_pages):
        i+=1
        pages.append(i)
    set2 = set(pages)
    set3 = set1.intersection(set2)
    pagelist = list(set3)
    if request.user.is_authenticated:
        products = Product.objects.filter(users_wishlist=request.user)
        wishlistcount = products.count()
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
    else:
        wishlistcount = ''
        cartprodcount = ''
    context = {
        'allprod':page_obj,
        'pagelist':pagelist,
        'currentpage':pn,
        'sortint':sortint,
        'wishlistcount': wishlistcount,
        'cartprodcount': cartprodcount,
        'sort': sort,
    }
    return render(request, 'home/productlist.html', context)

def productdetail(request, slug):
    log_activity(f"User {request.user.username if request.user.is_authenticated else 'Anonymous'} viewed details of product with slug {slug}")

    product = Product.objects.get(slug=slug)
    relatedprod = Product.objects.all().order_by('?')[:5]
    favoritemessage = ''
    if request.user.is_authenticated:
        products = Product.objects.filter(users_wishlist=request.user)
        wishlistcount = products.count()
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
        productexists = MyCart.objects.filter(user=request.user, product=product)
        if productexists.exists():
            productincart = 'Yes'
        else:
            productincart = 'No'
    else:
        wishlistcount = ''
        cartprodcount = ''
        productincart = ''
    if product.users_wishlist.filter(id=request.user.id).exists():
        favoritemessage = 'Remove From Favorites'
    else:
        favoritemessage = 'Add To Favorites'
    context = {
        'product':product,
        'relatedprod':relatedprod,
        'favoritemessage':favoritemessage,
        'wishlistcount': wishlistcount,
        'cartprodcount': cartprodcount,
        'productincart': productincart
    }
    return render(request, 'home/productdetail.html', context)

def search(request):
    log_activity(f"User {request.user.username if request.user.is_authenticated else 'Anonymous'} searched for '{request.GET.get('query')}'")

    db_logger = logging.getLogger('db')
    db_logger.info('info message %s' % request)
    db_logger.warning('warning message')  
    try:
         1/0 
    except Exception as e:
     db_logger.exception(e)

    query = request.GET.get('query') 
    if request.user.is_authenticated:
        products = Product.objects.filter(users_wishlist=request.user)
        wishlistcount = products.count()
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
    else:
        wishlistcount = ''
        cartprodcount = ''
    if len(query) > 30:
        products = Product.objects.none()
    else:
        product1 = Product.objects.filter(name__icontains=query)
        product2 = Product.objects.filter(desc__icontains=query)
        product3 = Product.objects.filter(tags__icontains=query)
        productf = product1.union(product2)
        products = productf.union(product3)
    context = {
        'allprod': products,
        'query':query,
        'wishlistcount': wishlistcount,
        'cartprodcount': cartprodcount,
    }
        
    return render(request, 'home/search.html', context)

def cart(request):
    otherprod = Product.objects.all().order_by('?')[:5]
    if request.user.is_authenticated:
        products = Product.objects.filter(users_wishlist=request.user)
        wishlistcount = products.count()
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
    else:
        wishlistcount = ''
        cartprodcount = ''
        cartprod = ''
    context = {
        'otherprod': otherprod,
        'wishlistcount': wishlistcount,
        'cartprod': cartprod,
        'cartprodcount': cartprodcount,
        }
    return render(request, 'home/cart.html', context)

@method_decorator(login_required, name='dispatch')
class Checkout(View):
    def get(self, request):
        form = CustomerForm()
        customers = Customer.objects.filter(user=request.user)
        if request.user.is_authenticated:
            products = Product.objects.filter(users_wishlist=request.user)
            wishlistcount = products.count()
            cartprod = MyCart.objects.filter(user=request.user)
            cartprodcount = cartprod.count()
        else:
            wishlistcount = ''
            cartprodcount = ''
            cartprod = ''
        return render(request, 'home/checkout.html', {'form':form, 'customers':customers, 'cartprod': cartprod,'wishlistcount': wishlistcount,'cartprodcount': cartprodcount,})

    def post(self, request):
        form = CustomerForm(request.POST)
        user = request.user
        customers = Customer.objects.filter(user=user)
        if request.user.is_authenticated:
            products = Product.objects.filter(users_wishlist=request.user)
            wishlistcount = products.count()
            cartprod = MyCart.objects.filter(user=request.user)
            cartprodcount = cartprod.count()
        else:
            wishlistcount = ''
            cartprodcount = ''
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            district = form.cleaned_data['district']
            address = form.cleaned_data['address']
            locality = form.cleaned_data['locality']
            phone_no = form.cleaned_data['phone_no']
            house_no = form.cleaned_data['house_no']
            zip_code = form.cleaned_data['zip_code']
            cus = Customer(user=user, full_name=full_name, district=district, address=address, locality=locality, phone_no=phone_no, house_no=house_no, zip_code=zip_code)
            cus.save()
            messages.success(request, 'Address/Customer added successfully!!')
            return redirect('checkout')
        # else:
        #     messages.success(request, 'Address/Customer added successfully!!')
        #     return redirect('home')
        messages.success(request, 'Error: Enter your correct phone number')
        return redirect('checkout')
        # return render(request, 'registration/checkout.html', {'form':form, 'customers':customers,'wishlistcount': wishlistcount,'cartprodcount': cartprodcount,})

@csrf_exempt
def add_to_wishlist(request):
    if request.method == 'POST':
        prod_id = request.POST.get('prod_id', '')
        product = get_object_or_404(Product, id=prod_id)
        message = ''
        if product.users_wishlist.filter(id=request.user.id).exists():
            product.users_wishlist.remove(request.user)
            message = 'removed'
        else:
            product.users_wishlist.add(request.user)
            message = 'added'
        data = {'message': message}
        return JsonResponse(data, safe=False)

def wishlist(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(users_wishlist=request.user)
        wishlistcount = products.count()
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
    else:
        wishlistcount = ''
        cartprodcount = ''
        products = ''
    context = {'products':products, 'wishlistcount': wishlistcount, 'cartprodcount':cartprodcount}
    return render(request, 'home/wishlist.html', context)

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        id = request.POST.get('prod_id')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(id=id)
        user = request.user
        mycart, created = MyCart.objects.get_or_create(user=user, product=product)
        if created:
            mycart.quantity = int(quantity)
        else:
            mycart.quantity += 1
        mycart.save()
        proqty = mycart.quantity
        selling_price = product.selling_price
        sub_total = proqty * product.selling_price
        cartproduct = [c for c in MyCart.objects.filter(user=request.user)]
        cartproducts = {}
        for i in range(len(cartproduct)):
            if cartproduct[i].id not in cartproducts.keys():
                cartproducts[cartproduct[i].id] = {
                    'cart_id': cartproduct[i].id,
                    'user_id':cartproduct[i].user.id,
                    'prod_id':cartproduct[i].product.id,
                    'prod_name': cartproduct[i].product.name,
                    'prod_weight': cartproduct[i].product.weight,
                    'prod_price': cartproduct[i].product.selling_price,
                    'prod_quantity': cartproduct[i].quantity,
                    'prod_image_url': cartproduct[i].product.photo.url,
                    }
        cartproductcount = MyCart.objects.filter(user=request.user).count()
        data = {'proqty':proqty, 'action':'add', 'selling_price':selling_price, 'sub_total': sub_total, 'cartproducts':cartproducts, 'cartproductcount':cartproductcount}
        return JsonResponse(data)

@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        id = request.POST.get('prod_id')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(id=id)
        user = request.user
        mycart = MyCart.objects.get(user=user, product=product)
        mycart.quantity -= int(quantity)
        mycart.save()
        proqty = mycart.quantity
        if mycart.quantity == 0:
            mycart.delete()
        product.save()
        selling_price = product.selling_price
        sub_total = proqty * product.selling_price
        product_id = product.id
        cartproduct = [c for c in MyCart.objects.filter(user=request.user)]
        cartproducts = {}
        for i in range(len(cartproduct)):
            if cartproduct[i].id not in cartproducts.keys():
                cartproducts[cartproduct[i].id] = {
                    'cart_id': cartproduct[i].id,
                    'user_id':cartproduct[i].user.id,
                    'prod_id':cartproduct[i].product.id,
                    'prod_name': cartproduct[i].product.name,
                    'prod_weight': cartproduct[i].product.weight,
                    'prod_price': cartproduct[i].product.selling_price,
                    'prod_quantity': cartproduct[i].quantity,
                    'prod_image_url': cartproduct[i].product.photo.url,
                    }
        cartproductcount = MyCart.objects.filter(user=request.user).count()
        data = {'product_id':product_id, 'proqty':proqty, 'action':'subt', 'selling_price':selling_price, 'sub_total': sub_total, 'cartproducts':cartproducts, 'cartproductcount':cartproductcount}
        return JsonResponse(data)

@csrf_exempt
def delete_from_cart(request):
    if request.method == 'POST':
        prod_id = request.POST.get('prod_id','')
        product = Product.objects.get(id=prod_id)
        product_cart = MyCart.objects.get(user=request.user, product=product)
        rowId = product_cart.product.id
        prod_sub_total = product_cart.sub_total
        product_cart.delete()
        cartproductcount = MyCart.objects.filter(user=request.user).count()
        data = {'rowId': rowId, 'prod_sub_total': prod_sub_total, 'cartproductcount': cartproductcount}
        return JsonResponse(data)

@login_required
def place_order(request):
    if request.method == 'POST':
        user = request.user
        customer_id = request.POST.get('address', '')
        unique_order_id = request.POST.get('unique-order-id', '')
        charge = request.POST.get('charge', '')
        promocode_text = request.POST.get('promocode', '')
        total_cost = request.POST.get('totalcost', '')
        actual_total_cost = int(total_cost)
        # payment_method = request.POST.get('payment-option', '') #For payment integration
        customer = Customer.objects.get(user=user, id=customer_id)
        # delivery_charge = 0
        delivery_charge = int(charge)
        promocode_discount_price = 0
        promocode = []
        if promocode_text != '':
            promocode = PromoCode.objects.filter(promo_code_text=promocode_text).first()
            if promocode:
                promocode_discount_price = promocode.promo_code_discount.discount_price
                promocode.delete()
        actual_total_cost -= promocode_discount_price
        cart_products = MyCart.objects.filter(user=user)
        if len(cart_products) == 0:
            return HttpResponseRedirect('/products/')

        ops = {}
        for c in cart_products:
            total_price = (c.product.selling_price * c.quantity)
            op = OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, total_price=total_price, unique_order_id=unique_order_id, delivery_charge=delivery_charge, total_cost=actual_total_cost, promo_discount=promocode_discount_price)
            op.save()
            #Decrease the available quantity of the product
            prod_available_qty = c.product.available_quantity
            c.product.available_quantity = prod_available_qty - c.quantity
            c.product.save()
            c.delete() #Deleting cart model after the order is placed

            # To customize email template
            opid = op.id
            realops = OrderPlaced.objects.get(id=opid)
            ops[realops.id] = {
                'cname':realops.customer.full_name,
                'caddress': realops.customer.district + ', ' + realops.customer.address + ', ' + realops.customer.locality,
                'opnameweightprice': [realops.product.name, realops.product.weight, 'Rs.' + str(realops.product.selling_price)],
                'opqty': realops.quantity,
                'subtotal': 'Rs.' + str(realops.quantity * realops.product.selling_price),
                'costdesc': ['Rs. ' + str(realops.total_cost), realops.promo_discount, 'Rs. ' + str(realops.delivery_charge)],
                }

        #Sending email to user
        html_template = render_to_string('emails/purchase_success_email.html', {'name':request.user.username, 'ops': ops})
        text_template = render_to_string('emails/purchase_success_email.txt', {'name':request.user.username, 'ops': ops})
        email = EmailMultiAlternatives(
            subject='Thank You For Your Purchase',
            body=text_template,
            from_email=settings.EMAIL_HOST_USER,
            to=[request.user.email,],
            reply_to=[settings.EMAIL_HOST_USER,]
        )
        email.attach_alternative(html_template, 'text/html')
        email.send(fail_silently=False)
        messages.success(request, 'Your purchase was placed successfully!!')
        return HttpResponseRedirect('/orders/')

def orders(request):
    if request.user.is_authenticated:
        user = request.user
        products = Product.objects.filter(users_wishlist=user)
        wishlistcount = products.count()
        cartprod = MyCart.objects.filter(user=user)
        cartprodcount = cartprod.count()
        orders = OrderPlaced.objects.filter(user=user).order_by('-id')
        forders = []
        for o in orders:
            ord = o.unique_order_id
            if(forders == []):
                forders.append([o])
            else:
                if(forders[-1][-1].unique_order_id == ord):
                    forders[-1].append(o)
                else:
                    forders.append([o])
    else:
        orders = ''
        wishlistcount = ''
        cartprodcount = ''
    context = {
        'orders':orders,
        'forders': forders,
        'wishlistcount': wishlistcount,
        'cartprodcount': cartprodcount,
    }
    return render(request, 'home/orders.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        preference = request.POST.get('preference')
        contact = Contact(full_name=name, email=email, phone=phone, preference=preference, message=message)
        contact.save()
        messages.success(request, 'Your message has been sent successfully!!')
        return redirect('home')
    return render(request, 'home/contact.html')

def subscription_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        SubscriptionEmail(email=email).save()
        messages.success(request, 'Thanks for subscribing HamroPasal!!')
        return redirect('home')

def about(request):
    return render(request, 'home/about.html')

def terms(request):
    return render(request, 'home/terms.html')

def skincare(request):
    sub_category = request.GET.get('sort', 0)
    sub_categoryint = int(sub_category)
    if sub_categoryint == 0:
        allprod = Product.objects.filter(category__title="Skin Care").order_by('-id')
    elif sub_categoryint == 1:
        allprod = Product.objects.filter(sub_category__title="Serum").order_by('-id')
    elif sub_categoryint == 2:
        allprod = Product.objects.filter(sub_category__title="Moisturizer").order_by('-id')
    elif sub_categoryint == 3:
        allprod = Product.objects.filter(sub_category__title="Night/Day Cream").order_by('-id')
    elif sub_categoryint == 4:
        allprod = Product.objects.filter(sub_category__title="Sunscreen").order_by('-id')
    elif sub_categoryint == 5:
        allprod = Product.objects.filter(sub_category__title="Toner").order_by('-id')
    elif sub_categoryint == 6:
        allprod = Product.objects.filter(sub_category__title="Acne Treatment").order_by('-id')
    elif sub_categoryint == 7:
        allprod = Product.objects.filter(sub_category__title="Other").order_by('-id')
    else:
        allprod = Product.objects.filter(category__title="Skin Care").order_by('-id')
    paginator = Paginator(allprod, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    total_pages = page_obj.paginator.num_pages
    pages = []
    pp = int(page_number) - 2
    p = int(page_number) - 1
    pn = int(page_number)
    n = int(page_number) + 1
    nn = int(page_number) + 2
    set1 = {pp, p, pn, n, nn}
    for i in range(total_pages):
        i+=1
        pages.append(i)
    set2 = set(pages)
    set3 = set1.intersection(set2)
    pagelist = list(set3)
    if request.user.is_authenticated:
        products = Product.objects.filter(users_wishlist=request.user)
        wishlistcount = products.count()
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
    else:
        wishlistcount = ''
        cartprodcount = ''
    context = {
        'allprod':page_obj,
        'pagelist':pagelist,
        'currentpage':pn,
        'sub_categoryint':sub_categoryint,
        'wishlistcount': wishlistcount,
        'cartprodcount': cartprodcount,
        'sort':sub_category,
    }
    return render(request, 'home/skincare.html', context)

def face(request):
    sub_category = request.GET.get('sort', 0)
    sub_categoryint = int(sub_category)
    if sub_categoryint == 0:
        allprod = Product.objects.filter(category__title="Face").order_by('?')
    elif sub_categoryint == 1:
        allprod = Product.objects.filter(sub_category__title="Primer").order_by('?')
    elif sub_categoryint == 2:
        allprod = Product.objects.filter(sub_category__title="Foundation").order_by('?')
    elif sub_categoryint == 3:
        allprod = Product.objects.filter(sub_category__title="Blush").order_by('?')
    elif sub_categoryint == 4:
        allprod = Product.objects.filter(sub_category__title="Cancealer").order_by('?')
    elif sub_categoryint == 5:
        allprod = Product.objects.filter(sub_category__title="Bronzer").order_by('?')
    else:
        allprod = Product.objects.filter(category__title="Body").order_by('?')
    paginator = Paginator(allprod, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    total_pages = page_obj.paginator.num_pages
    pages = []
    pp = int(page_number) - 2
    p = int(page_number) - 1
    pn = int(page_number)
    n = int(page_number) + 1
    nn = int(page_number) + 2
    set1 = {pp, p, pn, n, nn}
    for i in range(total_pages):
        i+=1
        pages.append(i)
    set2 = set(pages)
    set3 = set1.intersection(set2)
    pagelist = list(set3)
    if request.user.is_authenticated:
        products = Product.objects.filter(users_wishlist=request.user)
        wishlistcount = products.count()
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
    else:
        wishlistcount = ''
        cartprodcount = ''
    context = {
        'allprod':page_obj,
        'pagelist':pagelist,
        'currentpage':pn,
        'sub_categoryint':sub_categoryint,
        'wishlistcount': wishlistcount,
        'cartprodcount': cartprodcount,
        'sort':sub_category,
    }
    return render(request, 'home/face.html', context)

def body(request):
    sub_category = request.GET.get('sort', 0)
    sub_categoryint = int(sub_category)
    if sub_categoryint == 0:
        allprod = Product.objects.filter(category__title="Body").order_by('?')
    elif sub_categoryint == 1:
        allprod = Product.objects.filter(sub_category__title="Body Lotion").order_by('?')
    elif sub_categoryint == 2:
        allprod = Product.objects.filter(sub_category__title="Body Wash").order_by('?')
    elif sub_categoryint == 3:
        allprod = Product.objects.filter(sub_category__title="Deodorant").order_by('?')
    elif sub_categoryint == 4:
        allprod = Product.objects.filter(sub_category__title="Supplements").order_by('?')
    else:
        allprod = Product.objects.filter(category__title="Body").order_by('?')
    paginator = Paginator(allprod, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    total_pages = page_obj.paginator.num_pages
    pages = []
    pp = int(page_number) - 2
    p = int(page_number) - 1
    pn = int(page_number)
    n = int(page_number) + 1
    nn = int(page_number) + 2
    set1 = {pp, p, pn, n, nn}
    for i in range(total_pages):
        i+=1
        pages.append(i)
    set2 = set(pages)
    set3 = set1.intersection(set2)
    pagelist = list(set3)
    if request.user.is_authenticated:
        products = Product.objects.filter(users_wishlist=request.user)
        wishlistcount = products.count()
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
    else:
        wishlistcount = ''
        cartprodcount = ''
    context = {
        'allprod':page_obj,
        'pagelist':pagelist,
        'currentpage':pn,
        'sub_categoryint':sub_categoryint,
        'wishlistcount': wishlistcount,
        'cartprodcount': cartprodcount,
        'sort':sub_category,
    }
    return render(request, 'home/body.html', context)

def lips_and_eyes(request):
    sub_category = request.GET.get('sort', 0)
    sub_categoryint = int(sub_category)
    if sub_categoryint == 0:
        allprod = Product.objects.filter(category__title="Lips And Eyes").order_by('?')
    elif sub_categoryint == 1:
        allprod = Product.objects.filter(sub_category__title="Lipstick").order_by('?')
    elif sub_categoryint == 2:
        allprod = Product.objects.filter(sub_category__title="Liptint").order_by('?')
    elif sub_categoryint == 3:
        allprod = Product.objects.filter(sub_category__title="Lip Gloss").order_by('?')
    elif sub_categoryint == 4:
        allprod = Product.objects.filter(sub_category__title="Lip Liner").order_by('?')
    elif sub_categoryint == 5:
        allprod = Product.objects.filter(sub_category__title="Lips Mask").order_by('?')
    elif sub_categoryint == 6:
        allprod = Product.objects.filter(sub_category__title="Eye Shadow").order_by('?')
    elif sub_categoryint == 7:
        allprod = Product.objects.filter(sub_category__title="Mascara").order_by('?')
    elif sub_categoryint == 8:
        allprod = Product.objects.filter(sub_category__title="Eye Liner").order_by('?')
    else:
        allprod = Product.objects.filter(category__title="Lips And Eyes").order_by('?')
    paginator = Paginator(allprod, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    total_pages = page_obj.paginator.num_pages
    pages = []
    pp = int(page_number) - 2
    p = int(page_number) - 1
    pn = int(page_number)
    n = int(page_number) + 1
    nn = int(page_number) + 2
    set1 = {pp, p, pn, n, nn}
    for i in range(total_pages):
        i+=1
        pages.append(i)
    set2 = set(pages)
    set3 = set1.intersection(set2)
    pagelist = list(set3)
    if request.user.is_authenticated:
        products = Product.objects.filter(users_wishlist=request.user)
        wishlistcount = products.count()
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
    else:
        wishlistcount = ''
        cartprodcount = ''
    context = {
        'allprod':page_obj,
        'pagelist':pagelist,
        'currentpage':pn,
        'sub_categoryint':sub_categoryint,
        'wishlistcount': wishlistcount,
        'cartprodcount': cartprodcount,
        'sort':sub_category,
    }
    return render(request, 'home/lipsandeyes.html', context)

def hair(request):
    sub_category = request.GET.get('sort', 0)
    sub_categoryint = int(sub_category)
    if sub_categoryint == 0:
        allprod = Product.objects.filter(category__title="Hair").order_by('?')
    elif sub_categoryint == 1:
        allprod = Product.objects.filter(sub_category__title="Hair Treatment").order_by('?')
    elif sub_categoryint == 2:
        allprod = Product.objects.filter(sub_category__title="Hair Serum").order_by('?')
    elif sub_categoryint == 3:
        allprod = Product.objects.filter(sub_category__title="Hair Shampoo").order_by('?')
    elif sub_categoryint == 4:
        allprod = Product.objects.filter(sub_category__title="Hair Conditioner").order_by('?')
    else:
        allprod = Product.objects.filter(category__title="Hair").order_by('?')
    paginator = Paginator(allprod, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    total_pages = page_obj.paginator.num_pages
    pages = []
    pp = int(page_number) - 2
    p = int(page_number) - 1
    pn = int(page_number)
    n = int(page_number) + 1
    nn = int(page_number) + 2
    set1 = {pp, p, pn, n, nn}
    for i in range(total_pages):
        i+=1
        pages.append(i)
    set2 = set(pages)
    set3 = set1.intersection(set2)
    pagelist = list(set3)
    if request.user.is_authenticated:
        products = Product.objects.filter(users_wishlist=request.user)
        wishlistcount = products.count()
        cartprod = MyCart.objects.filter(user=request.user)
        cartprodcount = cartprod.count()
    else:
        wishlistcount = ''
        cartprodcount = ''
    context = {
        'allprod':page_obj,
        'pagelist':pagelist,
        'currentpage':pn,
        'sub_categoryint':sub_categoryint,
        'wishlistcount': wishlistcount,
        'cartprodcount': cartprodcount,
        'sort':sub_category,
    }
    return render(request, 'home/hair.html', context)