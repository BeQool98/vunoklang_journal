from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name="home"),
 
    # path('login/', login_user, name="login"),
    path('about/', about_page, name="about"),
    path('contact_message/', contact_message, name="contact_message"),
    path('book-details/<slug:slug>', BookDetail.as_view(), name="book_detail"),
    path('download/<int:document_id>', download, name="download"),
    path('search/', search, name="search"),
    path('category/<str:title>/', category_id, name="category_id"),


   
] 

   