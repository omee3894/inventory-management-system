from django.urls import path
from .views import login_page, dashboard, product_list, add_product, delete_product, edit_product, update_stock, billing 
urlpatterns = [
    path('', login_page),
    path('dashboard/', dashboard),
    path('products/', product_list),
    path('add-product/', add_product),
    path('delete-product/<int:id>/', delete_product),
    path('edit-product/<int:id>/', edit_product),
    path('stock/<int:id>/', update_stock),
    path('billing/', billing),
    path('create-admin/', views.create_admin),
]