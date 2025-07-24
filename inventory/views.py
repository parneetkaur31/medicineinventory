from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Customer
from django.utils import timezone
from django.shortcuts import render,redirect, get_object_or_404
from .models import Category
from .models import Product, Category, Vendor
from .models import PurchaseDetail, Purchase, Product
from .models import SaleDetail, Sale, Product
from django.db.utils import IntegrityError

from django.db.models import Sum
from decimal import Decimal
from datetime import date
from django.db.models import F
from django.db.models import Q






def render_with_segment(request, template_path, segment_name):
    context = {'segment': segment_name}
    return render(request, template_path, context)

def dashboard_view(request):
    low_stock_products = Product.objects.filter(quantity__lt=F('min_reorder_quantity'))
    return render(request, 'pages/dashboard.html', {'low_stock_products': low_stock_products})


from datetime import date

def dashboard(request):
    low_stock_products = Product.objects.filter(quantity__lt=F('min_reorder_quantity'))
    
    # Counts
    vendor_count = Vendor.objects.count()
    product_count = Product.objects.count()
    customer_count = Customer.objects.count()

    today = date.today()

    # Today's Purchases
    todays_purchases = Purchase.objects.filter(purchase_date=today)

    # Today's Sales - Ensure Sale model has sale_date
    todays_sales = Sale.objects.filter(sale_date=today)

    context = {
        'low_stock_products': low_stock_products,
        'vendor_count': vendor_count,
        'product_count': product_count,
        'customer_count': customer_count,
        'todays_purchases': todays_purchases,
        'todays_sales': todays_sales,
    }

    return render(request, 'pages/dashboard.html', context)
def charts(request):
    return render_with_segment(request, 'charts/index.html', 'charts')

def icons(request):
    return render_with_segment(request, 'pages/icons.html', 'icons')

def map(request):
    return render_with_segment(request, 'pages/map.html', 'map')

def notifications(request):
    return render_with_segment(request, 'pages/notifications.html', 'notifications')

def user_profile(request):
    return render_with_segment(request, 'pages/user.html', 'user_profile')

def tables(request):
    return render_with_segment(request, 'pages/tables.html', 'tables')

def typography(request):
    return render_with_segment(request, 'pages/typography.html', 'typography')

def dynamic_dt(request):
    return render_with_segment(request, 'dyn_dt/index.html', 'dynamic_dt')

def dynamic_api(request):
    return render_with_segment(request, 'dyn_api/index.html', 'dynamic_api')

from django.contrib.auth import authenticate, login

def auth_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        form = UserCreationForm(request.POST)  

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif len(password1) < 6:
            messages.error(request, "Password must be at least 6 characters.")
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                
                authenticated_user = authenticate(request, username=username, password=password1)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    return redirect('dashboard')
                else:
                    messages.error(request, "Authentication failed. Please try logging in manually.")
                    return redirect('auth_signin')

            except ValidationError as e:
                messages.error(request, f"Error: {e}")

    else:
        form = UserCreationForm()

    return render(request, 'pages/signup.html', {'form': form, 'segment': 'auth_signup'})


def logout_view(request):
    logout(request)
    return redirect('auth_signin')

class CustomLoginView(DjangoLoginView):
    template_name = 'pages/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'auth_signin'
        return context
def customers(request):
    if request.method == "POST":
        try:
            Customer.objects.create(
                name=request.POST['name'],
                address=request.POST['address'],
                phone=request.POST['phone']
            )
            messages.success(request, "Customer added successfully.")
        except IntegrityError:
            messages.error(request, "Phone number already exists. Please enter a unique phone number.")
    
    customers = Customer.objects.all()
    return render(request, 'pages/customers.html', {'customers': customers})
from django.shortcuts import redirect, get_object_or_404
from .models import Customer

def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()
    return redirect('customers')
def categories_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            messages.success(request, "Category added successfully.")
            return redirect('categories')
    categories = Category.objects.all()
    return render(request, 'pages/categories.html', {'categories': categories})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect('categories')

def products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        vendor_id = request.POST.get('vendor')
        mrp = request.POST.get('mrp')
        company = request.POST.get('company')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        color = request.POST.get('color')
        weight = request.POST.get('weight')
        stock_value = request.POST.get('stock_value')
        min_reorder_quantity = request.POST.get('min_reorder_quantity')
        is_available = request.POST.get('is_available') == 'True'

        category = Category.objects.get(id=category_id)
        vendor = Vendor.objects.get(id=vendor_id) if vendor_id else None

        Product.objects.create(
            
            name=name,
            category=category,
            vendor=vendor,
            mrp=mrp,
            company=company,
            description=description,
            quantity=quantity,
            color=color,
            weight=weight,
            stock_value=stock_value,
            min_reorder_quantity=min_reorder_quantity,
            is_available=is_available
        )
        return redirect('products')

    return render(request, 'pages/products.html', {
        'products': products,
        'categories': categories,
        'vendors': vendors
    })


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('products')
def products_view(request):
    products = Product.objects.all()
    return render(request, 'pages/products.html', {'products': products, 'segment': 'products'})
def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if name:
            category.name = name
            category.save()
            messages.success(request, "Category updated successfully.")
        else:
            messages.error(request, "Category name cannot be empty.")
        
        return redirect('categories')  

    return redirect('categories')
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.address = request.POST.get('address')
        customer.phone = request.POST.get('phone')
        customer.save()
        
    return redirect('customers')
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category_id = request.POST.get('category')
        product.vendor_id = request.POST.get('vendor') or None
        product.mrp = request.POST.get('mrp')
        product.company = request.POST.get('company')
        product.description = request.POST.get('description')
        product.quantity = request.POST.get('quantity')
        product.color = request.POST.get('color')
        product.weight = request.POST.get('weight')
        product.stock_value = request.POST.get('stock_value')
        product.min_reorder_quantity = request.POST.get('min_reorder_quantity')
        product.is_available = request.POST.get('is_available') == 'True'
        product.save()
        
    return redirect('products')
def purchases(request):
    if request.method == 'POST':
        Purchase.objects.create(
            vendor=get_object_or_404(Vendor, id=request.POST.get('vendor')),
            purchase_date=request.POST.get('purchase_date'),
            bill_no=request.POST.get('bill_no'),
            total=request.POST.get('total'),
            gst_rate=request.POST.get('gst_rate'),
            gst_amount=request.POST.get('gst_amount'),
            discount_rate=request.POST.get('discount_rate'),
            discount_amount=request.POST.get('discount_amount'),
            net_amount=request.POST.get('net_amount')
        )
        return redirect('purchases')

    purchases = Purchase.objects.all()
    vendors = Vendor.objects.all()
    return render(request, 'pages/purchases.html', {'purchases': purchases, 'vendors': vendors})


def purchasedetails(request):
    if request.method == "POST":
        purchase_id = request.POST.get("purchase")
        product_id = request.POST.get("product")
        purchase_quantity = int(request.POST.get("purchase_quantity"))
        purchase_rate = float(request.POST.get("purchase_rate"))
        
        purchase = Purchase.objects.get(id=purchase_id)
        product = Product.objects.get(id=product_id)

        purchase_amount = purchase_quantity * purchase_rate  

        existing_total = PurchaseDetail.objects.filter(purchase=purchase).aggregate(Sum('purchase_amount'))['purchase_amount__sum'] or 0

        purchase_amount = request.POST.get('purchase_amount')
        purchase_amount = Decimal(purchase_amount) if purchase_amount else Decimal('0')

        if existing_total + purchase_amount > purchase.net_amount:
            messages.error(request, "Total purchase amount exceeds net amount of the purchase.")
            return redirect('purchasedetails')

        PurchaseDetail.objects.create(
            purchase=purchase,
            product=product,
            purchase_quantity=purchase_quantity,
            purchase_rate=purchase_rate,
            purchase_amount=purchase_amount
        )

       
        product.quantity += purchase_quantity
        product.save()

        messages.success(request, "Purchase detail added successfully.")
        return redirect('purchasedetails')

    purchases = Purchase.objects.all()
    products = Product.objects.all()
    purchasedetails = PurchaseDetail.objects.all()

    return render(request, 'pages/purchasedetails.html', {
        'purchases': purchases,
        'products': products,
        'purchasedetails': purchasedetails
    })


def delete_purchasedetail(request, id):
    purchasedetail = get_object_or_404(PurchaseDetail, id=id)
    purchasedetail.delete()
    return redirect('purchasedetails')

def update_purchasedetail(request, id):
    purchasedetail = get_object_or_404(PurchaseDetail, id=id)

    if request.method == 'POST':
        purchase_id = request.POST.get('purchase')
        product_id = request.POST.get('product')
        purchase_quantity = request.POST.get('purchase_quantity')
        purchase_rate = request.POST.get('purchase_rate')

        purchase = Purchase.objects.get(id=purchase_id)
        product = Product.objects.get(id=product_id)

        purchase_amount = float(purchase_quantity) * float(purchase_rate)

        
        existing_total = PurchaseDetail.objects.filter(purchase=purchase).exclude(id=id).aggregate(Sum('purchase_amount'))['purchase_amount__sum'] or 0

        if existing_total + purchase_amount > float(purchase.net_amount):
            messages.error(request, "Total purchase amount exceeds net amount of the purchase.")
            return redirect('purchasedetails')

        purchasedetail.purchase = purchase
        purchasedetail.product = product
        purchasedetail.purchase_quantity = purchase_quantity
        purchasedetail.purchase_rate = purchase_rate
        purchasedetail.purchase_amount = purchase_amount
        purchasedetail.save()

    return redirect('purchasedetails')


def update_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    if request.method == 'POST':
        purchase.vendor = get_object_or_404(Vendor, id=request.POST.get('vendor'))
        purchase.bill_no = request.POST.get('bill_no')
        purchase.total = request.POST.get('total')
        purchase.net_amount = request.POST.get('net_amount')
        purchase.save()
        return redirect('purchases')


def delete_purchase(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    purchase.delete()
    return redirect('purchases')
def sale_details(request):
    sales = Sale.objects.all()
    products = Product.objects.all()
    sale_details = SaleDetail.objects.all().order_by('-id')

    if request.method == 'POST':
        try:
            sale_id = request.POST['sale']
            product_id = request.POST['product']
            quantity = float(request.POST['sale_quantity'])
            rate = float(request.POST['sale_rate'])
            amount = float(request.POST['sale_amount'])

            sale = Sale.objects.get(id=sale_id)
            product = Product.objects.get(id=product_id)

            existing_total = SaleDetail.objects.filter(sale=sale).aggregate(Sum('sale_amount'))['sale_amount__sum'] or 0

            if existing_total + amount > float(sale.net_amount):
                messages.error(request, "Total sale amount exceeds Net Amount for this Sale.")
                return redirect('sale_details')

           
            if quantity > product.quantity:
                messages.error(request, "Insufficient stock for this product.")
                return redirect('sale_details')

            SaleDetail.objects.create(
                sale=sale,
                product=product,
                sale_quantity=quantity,
                sale_rate=rate,
                sale_amount=amount
            )

           
            product.quantity -= quantity
            product.save()

            messages.success(request, "Sale detail added successfully!")
            return redirect('sale_details')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('sale_details')

    context = {
        'sales': sales,
        'products': products,
        'sale_details': sale_details
    }
    return render(request, 'pages/sale_details.html', context)


def update_sale_detail(request, id):
    detail = get_object_or_404(SaleDetail, id=id)
    
    if request.method == 'POST':
        sale_id = request.POST.get('sale')
        product_id = request.POST.get('product')
        quantity = float(request.POST.get('sale_quantity'))
        rate = float(request.POST.get('sale_rate'))
        amount = float(request.POST.get('sale_amount'))

        sale = Sale.objects.get(id=sale_id)
        product = Product.objects.get(id=product_id)

       
        existing_total = SaleDetail.objects.filter(sale=sale).exclude(id=id).aggregate(Sum('sale_amount'))['sale_amount__sum'] or 0

        if existing_total + amount > float(sale.net_amount):
            messages.error(request, "Total sale amount exceeds Net Amount for this Sale.")
            return redirect('sale_details')

        detail.sale = sale
        detail.product = product
        detail.sale_quantity = quantity
        detail.sale_rate = rate
        detail.sale_amount = amount
        detail.save()

        messages.success(request, "Sale detail updated successfully!")
    
    return redirect('sale_details')


def delete_sale_detail(request, id):
    detail = get_object_or_404(SaleDetail, id=id)
    detail.delete()
    return redirect('sale_details')
from django.db import IntegrityError
from django.contrib import messages

def sales(request):
    sales = Sale.objects.all().order_by('-id')  
    customers = Customer.objects.all()

    if request.method == "POST":
        customer_id = request.POST['customer']
        invoice_no = request.POST['invoice_no']
        total = float(request.POST['total'])
        gst_rate = float(request.POST['gst_rate'])
        discount_rate = float(request.POST['discount_rate'])

        gst_amount = total * gst_rate / 100
        discount_amount = total * discount_rate / 100
        net_amount = total + gst_amount - discount_amount

        customer = Customer.objects.get(id=customer_id)

        try:
            Sale.objects.create(
                customer=customer,
                invoice_no=invoice_no,
                total=total,
                gst_rate=gst_rate,
                gst_amount=gst_amount,
                discount_rate=discount_rate,
                discount_amount=discount_amount,
                net_amount=net_amount
            )
            messages.success(request, "Sale added successfully!")
            return redirect('sales')
            
        except IntegrityError:
            messages.error(request, "Invoice number already exists. Please use a unique invoice number.")

    context = {
        'sales': sales,
        'customers': customers
    }
    return render(request, 'pages/sales.html', context)



def update_sale(request, id):
    sale = get_object_or_404(Sale, id=id)
    
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        invoice_no = request.POST.get('invoice_no')
        total = request.POST.get('total')
        gst_rate = request.POST.get('gst_rate')
        gst_amount = request.POST.get('gst_amount')
        discount_rate = request.POST.get('discount_rate')
        discount_amount = request.POST.get('discount_amount')
        net_amount = request.POST.get('net_amount')

        try:
            sale.customer = Customer.objects.get(id=customer_id)
            sale.invoice_no = invoice_no
            sale.total = total
            sale.gst_rate = gst_rate
            sale.gst_amount = gst_amount
            sale.discount_rate = discount_rate
            sale.discount_amount = discount_amount
            sale.net_amount = net_amount
            sale.save()
            messages.success(request, "Sale updated successfully.")
        except:
            messages.error(request, "Error updating sale.")
        
        return redirect('sales')

    return redirect('sales')


def delete_sale(request, id):
    sale = get_object_or_404(Sale, id=id)
    sale.delete()
    messages.success(request, "Sale deleted successfully.")
    return redirect('sales')
def vendors(request):
    vendors = Vendor.objects.all().order_by('-id')

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gst_number = request.POST.get('gst_number')
        is_active = request.POST.get('is_active') == 'True'

        if Vendor.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif Vendor.objects.filter(gst_number=gst_number).exists():
            messages.error(request, "GST number already exists.")
        else:
            Vendor.objects.create(
                name=name,
                address=address,
                phone=phone,
                email=email,
                gst_number=gst_number,
                is_active=is_active
            )
            messages.success(request, "Vendor added successfully!")
        return redirect('vendors')

    return render(request, 'pages/vendors.html', {'vendors': vendors})


def update_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)

    if request.method == 'POST':
        vendor.name = request.POST.get('name')
        vendor.address = request.POST.get('address')
        vendor.phone = request.POST.get('phone')
        vendor.email = request.POST.get('email')
        vendor.gst_number = request.POST.get('gst_number')
        vendor.is_active = request.POST.get('is_active') == 'True'
        vendor.save()

        messages.success(request, "Vendor updated successfully!")
        return redirect('vendors')

    return redirect('vendors')


def delete_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    vendor.delete()
    messages.success(request, "Vendor deleted successfully.")
    return redirect('vendors')

def sale_report(request):
    sales = Sale.objects.all()
    products = Product.objects.all()

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    product_id = request.GET.get('product')

    if from_date and to_date:
        sales = sales.filter(sale_date__range=[from_date, to_date])

    if product_id:
        sales = sales.filter(saledetail__product_id=product_id).distinct()

    context = {
        'sales': sales,
        'products': products,
    }
    return render(request, 'pages/sale_report.html', context)


def purchase_report(request):
    purchases = Purchase.objects.all()
    products = Product.objects.all()

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    product_id = request.GET.get('product')

    if from_date and to_date:
        purchases = purchases.filter(purchase_date__range=[from_date, to_date])

    if product_id:
        purchases = purchases.filter(purchasedetail__product_id=product_id).distinct()

    context = {
        'purchases': purchases,
        'products': products,
    }
    return render(request, 'pages/purchase_report.html', context)
def sale_report_detail(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    sale_details = SaleDetail.objects.filter(sale=sale)
    return render(request, 'pages/sale_report_detail.html', {'sale': sale, 'sale_details': sale_details})


def purchase_report_detail(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)
    purchase_details = PurchaseDetail.objects.filter(purchase=purchase)
    return render(request, 'pages/purchase_report_detail.html', {'purchase': purchase, 'purchase_details': purchase_details})
