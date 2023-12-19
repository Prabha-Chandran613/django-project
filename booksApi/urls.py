from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list),
    path('books/create/', views.create_book),
    path('books/<int:pk>/', views.view_book),
    path('books/update/<int:pk>/', views.update_book),
    path('books/delete/<int:pk>/', views.delete_book),
]
