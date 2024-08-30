from django.urls import path
from . import views

urlpatterns=[
    path('' ,views.home,name='home'),
    path('products/' ,views.products,name='products'),
    path('productdetails/' ,views.productdetails,name='productdetails'),
    path('contact/' ,views.contact,name='contact'),
    path('cart/',views.cart,name='cart'),
    path('account/', views.login_view,name='account'),
    path('signup/', views.signup ,name='signup'),
    
]