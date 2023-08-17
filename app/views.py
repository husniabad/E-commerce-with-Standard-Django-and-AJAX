from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.views import View
from . models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist,Categories
from . forms import CustomerRegistrationForm,CustomerProfileForm
from django.db.models import Count
from django.http import JsonResponse,HttpResponse
from django.db.models import Q
from django.conf import settings
import razorpay
from django.contrib import messages
from django.db.models import Sum
import time

#for category symbol replace
from django.db.models import CharField, Value
from django.db.models import Case, CharField, Value, When
from .models import CATEGORY_CHOICES


def home(request):
    total_quantity = 0
    wishitem = 0
    if request.user.is_authenticated:
        
        total_quantity = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        total_quantity = total_quantity or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
        # totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/home.html",locals())

def home2(request):
    
    total_quantity = 0
    wishitem = 0
    if request.user.is_authenticated:
        
        total_quantity = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        total_quantity = total_quantity or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
        # totalitem = len(Cart.objects.filter(user=request.user))
    category20 = Product.objects.get(id=20)
    category_key = 'ML'  # Key to retrieve the category value
    category_value = None
    
    categories = Categories.objects.all()
    when_choices = [When(category=code, then=Value(choice)) for code, choice in CATEGORY_CHOICES]
    
    categories = categories.annotate(
        category_name=Case(*when_choices, output_field=CharField())
    )

    product = Product.objects.all()
    when_choices = [When(category=code, then=Value(choice)) for code, choice in CATEGORY_CHOICES]
    
    product = product.annotate(
        category_name=Case(*when_choices, output_field=CharField())
    )

    # Milk
    milk = product.filter(category='ML')
    for prod in milk:
            if prod.discounted_price != 0:
                prod.percentage_off = round((prod.selling_price - prod.discounted_price) / prod.selling_price * 100)
                
            else:
                prod.percentage_off = 0

            prod.wishlist = Wishlist.objects.filter(product=prod, user=request.user)
            cart_item = Cart.objects.filter(user=request.user, product=prod).first()
    # New Added
    new_added = product.order_by('-id')[:8]

    for prod in new_added:
            if prod.discounted_price != 0:
                prod.percentage_off = round((prod.selling_price - prod.discounted_price) / prod.selling_price * 100)
                
            else:
                prod.percentage_off = 0

            prod.wishlist = Wishlist.objects.filter(product=prod, user=request.user)
            cart_item = Cart.objects.filter(user=request.user, product=prod).first()
    

    # when_choices = [When(category=code, then=Value(choice)) for code, choice in CATEGORY_CHOICES]

    # categories = categories.annotate(
    # category_choice=Case(*when_choices, output_field=CharField())
    # )
    # for category_values in categories:
    #     category_values.category = category_values.category_choice

    return render(request, "app/home2.html",locals())



def about(request):
    total_quantity = 0
    wishitem = 0
    if request.user.is_authenticated:
        
        total_quantity = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        total_quantity = total_quantity or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
        # totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/about.html",locals())

def contact(request):
    total_quantity = 0
    wishitem = 0
    if request.user.is_authenticated:
        
        total_quantity = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        total_quantity = total_quantity or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
        # totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/contact.html",locals())

class CategoryView(View):
    def get(self, request,val):
        total_quantity = 0
        wishitem = 0
        if request.user.is_authenticated:
            total_quantity = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
            total_quantity = total_quantity or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
            # totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        print("product: ",product)

        # productz = Product.objects.get(pk=pk)
        # wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        title = product.values('title')

        for prod in product:
            if prod.discounted_price != 0:
                prod.percentage_off = round((prod.selling_price - prod.discounted_price) / prod.selling_price * 100)
                
            else:
                prod.percentage_off = 0

            prod.wishlist = Wishlist.objects.filter(product=prod, user=request.user)
            # product.wishlist = wishlist
            # print ("wishlist: ",wishlist)
        

        # print('val:', val)
        
        return render(request, "app/category.html", locals()) 
    
class ProductDetail(View):
    def get(self, request,pk):
        total_quantity = 0
        wishitem = 0
        if request.user.is_authenticated:
            
            total_quantity = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
            total_quantity = total_quantity or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
            # totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.get(pk=pk)
        print('product: ', product)
        
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))

        print("wishlist: ", wishlist)
        
        # print('prod: ', wishlist.values())
        if product.discounted_price != 0:
            percentage_off = round((product.selling_price - product.discounted_price) / product.selling_price * 100)
        else:
            percentage_off = 0

        cart_item = Cart.objects.filter(user=request.user, product=product).first()
        print("cart items",cart_item)
        return render(request, "app/productdetail.html", locals())
    
class CategoryTitle(View):
    def get(self, request, val):
        total_quantity = 0
        wishitem = 0
        if request.user.is_authenticated:
        
            total_quantity = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
            total_quantity = total_quantity or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
            # totalitem = len(Cart.objects.filter(user=request.user))
        
        
        # if products.discounted_price != 0:
        #     percentage_off = round((products.selling_price - products.discounted_price) / products.selling_price * 100)
        # else:
        #     percentage_off = 0
        product = Product.objects.filter(title=val)
        for prod in product:
            print('Product: ', prod)
            if prod.discounted_price != 0:
                prod.percentage_off = round((prod.selling_price - prod.discounted_price) / prod.selling_price * 100)
                
            else:
                prod.percentage_off = 0
            prod.wishlist = Wishlist.objects.filter(product=prod, user=request.user)


        title = Product.objects.filter(category = product[0].category).values('title')
        return render(request, "app/category.html",locals())
    

class CustomerRegistrationView(View):
    def get(self, request):
        total_quantity = 0
        wishitem = 0
        if request.user.is_authenticated:
        
            total_quantity = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
            total_quantity = total_quantity or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
            # totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"User registered successfully!")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/customerregistration.html',locals())
    
class ProfileView(View):
    def get(self, request):
        total_quantity = 0
        wishitem = 0
        if request.user.is_authenticated:
        
            total_quantity = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
            total_quantity = total_quantity or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
            # totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality,mobile=mobile, city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Data Added Successfully!")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/profile.html',locals())
    
#use function when only fetch data from db and display class for get/post , save/update data from db)
def address(request):
    total_quantity = 0
    wishitem = 0
    if request.user.is_authenticated:
    
        total_quantity = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        total_quantity = total_quantity or 0
        wishitem = len(Wishlist.objects.filter(user=request.user))
        # totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user = request.user)
    return render(request, 'app/address.html',locals())

class updateAddress(View):
    def get(self, request,pk):
        total_quantity = 0
        wishitem = 0
        if request.user.is_authenticated:
        
            total_quantity = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
            total_quantity = total_quantity or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
            # totalitem = len(Cart.objects.filter(user=request.user))
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
        
            messages.success(request,"Profile Updated Successfully!")
        else:
            messages.warning(request, "Invalid Input Data")
        time.sleep(1)
        return redirect('address')
    

# cart 

from django.http import JsonResponse

def add_to_cart(request):
    if request.user.is_authenticated:
        product_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=product_id)

        # Check if the product already exists in the user's cart
        if Cart.objects.filter(user=request.user, product=product).exists():
            messages.warning(request, 'Product already exists in the cart.')
            c = Cart.objects.get(Q(product = product) & Q(user = request.user))
            

            data = {
                'message': 'Product added to the cart.',
                'quantity': c.quantity,
            }

            # Return a JSON response with the success message and quantity
            return JsonResponse(data)
        else:
            Cart.objects.create(user=request.user, product=product)
            messages.success(request, 'Product added to the cart.')
            # c = Cart.objects.filter(user=request.user, product=product)
            c = Cart.objects.get(Q(product = product) & Q(user = request.user))
            

            data = {
                'message': 'Product added to the cart.',
                'quantity': c.quantity,
            }

            # Return a JSON response with the success message and quantity
            return JsonResponse(data)
    else:
        return JsonResponse({'message': 'User not authenticated.'})



def show_cart(request):
    total_quantity = 0
    wishitem = 0
    if request.user.is_authenticated:
    
        total_quantity = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        total_quantity = total_quantity or 0    
        wishitem = len(Wishlist.objects.filter(user=request.user))
        # totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    print("cart",cart)
    amount = 0
    for prod in cart:
        value = prod.quantity * prod.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
   
    return render(request, 'app/addtocart.html',locals())

class checkout(View):
    def get(self, request):
        total_quantity = 0
        wishitem = 0
        if request.user.is_authenticated:
        
            total_quantity = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']
            total_quantity = total_quantity or 0
            wishitem = len(Wishlist.objects.filter(user=request.user))
            # totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for prod in cart_items:
            value = prod.quantity * prod.product.discounted_price
            famount = famount + value
            
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency":"INR","receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'id': 'order_Lvo8WFtdlzhyyb', 'entity': 'order', 'amount': 27500, 'amount_paid': 0, 'amount_due': 27500, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1685435168}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status,
            )
            payment.save()
        return render(request, 'app/checkout.html',locals())

def payment_done(request):
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    # print("orid: ",order_id, "paid: ",payment_id, "custid: ",cust_id)

    user=request.user
    # return redirect("orders")

    customer = Customer.objects.get(id=cust_id) #update payment status and id

    payment= Payment.objects.get(razorpay_order_id = order_id)
    payment.paid = True
    payment.razorpay_order_id = payment_id
    payment.save()

    cart = Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity = c.quantity, payment=payment).save()
        c.delete()
    return redirect("orders")

def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        wishitem = len(Wishlist.objects.filter(user=request.user))
        totalitem = len(Cart.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity+=1
        c.save() 
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        # print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount' : totalamount,
        }
        return JsonResponse(data)
    

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity-=1
        c.save() 
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        # print(prod_id)
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount' : totalamount,
        }
        return JsonResponse(data)
    
def get_quantity(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        data={
            'quantity':c.quantity,
        }
        return JsonResponse(data)
    

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        # print(prod_id)
        data={
            'amount':amount,
            'totalamount' : totalamount,
        }
        return JsonResponse(data)
    
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id = prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'Wishlist Added successfully',
        }
        return JsonResponse(data)

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id = prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message':'Wishlist Added successfully',
        }
        return JsonResponse(data)
  