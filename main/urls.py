from django.urls import path
from .views import login_page, dashboard, product_list, add_product, delete_product, edit_product, update_stock, billing, create_admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', login_page),
    path('dashboard/', dashboard),
    path('products/', product_list),
    path('add-product/', add_product),
    path('delete-product/<int:id>/', delete_product),
    path('edit-product/<int:id>/', edit_product),
    path('stock/<int:id>/', update_stock),
    path('billing/', billing),
    path('create-admin/', create_admin),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('invoice/<int:bill_id>/', views.invoice, name='invoice'),
]