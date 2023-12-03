from django.urls import path
from .import views  

urlpatterns = [
    
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('management/', views.management, name='management'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path("product/add", views.add, name="add"),
    path("product/delete/<int:id>", views.delete, name="delete"),
    path('product/detalle/<int:id>', views.detalle, name='detalle'),
    path('product/update/<int:id>', views.update, name='update'),
    path('product/<int:pk>', views.product, name='product'),
]