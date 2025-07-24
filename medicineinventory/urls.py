from django.contrib import admin
from django.urls import path
from inventory import views
from inventory.views import (
    dashboard, charts, icons, map, notifications, user_profile,
    tables, typography, dynamic_dt, dynamic_api, auth_signup, logout_view, CustomLoginView, customers, delete_customer,delete_category, categories_view,delete_product,update_category
)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('categories/update/<int:category_id>/', views.update_category, name='update_category'),
    path('products/update/<int:product_id>/', views.update_product, name='update_product'),
    path('purchasedetails/', views.purchasedetails, name='purchasedetails'),
    path('vendors/', views.vendors, name='vendors'),
    path('vendors/update/<int:vendor_id>/', views.update_vendor, name='update_vendor'),
    path('vendors/delete/<int:vendor_id>/', views.delete_vendor, name='delete_vendor'),

path('delete_purchasedetail/<int:id>/', views.delete_purchasedetail, name='delete_purchasedetail'),
path('update_purchasedetail/<int:id>/', views.update_purchasedetail, name='update_purchasedetail'),
 path('purchases/', views.purchases, name='purchases'),
    path('update_purchase/<int:purchase_id>/', views.update_purchase, name='update_purchase'),
    path('delete_purchase/<int:purchase_id>/', views.delete_purchase, name='delete_purchase'),
      path('sale-details/', views.sale_details, name='sale_details'),
    path('update-sale-detail/<int:id>/', views.update_sale_detail, name='update_sale_detail'),
    path('delete-sale-detail/<int:id>/', views.delete_sale_detail, name='delete_sale_detail'),
path('reports/sale/', views.sale_report, name='sale_report'),
path('reports/purchase/', views.purchase_report, name='purchase_report'),
path('reports/sale/<int:sale_id>/', views.sale_report_detail, name='sale_report_detail'),
path('reports/purchase/<int:purchase_id>/', views.purchase_report_detail, name='purchase_report_detail'),






 path('customers/update/<int:customer_id>/', views.update_customer, name='update_customer'),
    path('admin/', admin.site.urls),
     path('customers/', customers, name='customers'),
     path('customers/delete/<int:customer_id>/', delete_customer, name='delete_customer'),
     path('categories/', views.categories_view, name='categories'),
path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('products/', views.products, name='products'),
path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
path('sales/', views.sales, name='sales'),
    path('update-sale/<int:id>/', views.update_sale, name='update_sale'),
    path('delete-sale/<int:id>/', views.delete_sale, name='delete_sale'),



    # Pages
   path('', dashboard, name='dashboard'),

    path('charts/', charts, name='charts'),
    path('icons/', icons, name='icons'),
    path('map/', map, name='map'),
    path('notifications/', notifications, name='notifications'),
    path('profile/', user_profile, name='user_profile'),
    path('tables/', tables, name='tables'),
    path('typography/', typography, name='typography'),

    # Dynamic
    path('dynamic/', dynamic_dt, name='dynamic_dt'),
    path('dynamic-api/', dynamic_api, name='dynamic_api'),

    # Auth
    path('signin/', CustomLoginView.as_view(), name='auth_signin'),
    path('signup/', auth_signup, name='auth_signup'),
    path('logout/', logout_view, name='logout'),

    # Password change (optional)
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='auth/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'), name='password_change_done'),
]
