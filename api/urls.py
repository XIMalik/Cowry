from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', Register.as_view(), name="register"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('add-book/', add_book, name='add-book'),
    path('delete-book/', delete_book, name='delete-book'),
    
    path('all-books/', ListBooks.as_view(), name='all-books'),
    path('book/<str:book_id>/', GetSingleBook.as_view(), name='get-single-book'),
    path('books/filter/', FilterBooks.as_view(), name='filter-books'),
    path('borrow/', BorrowBook.as_view(), name='borrow-book'),

    path('all-users/', AllUsers.as_view(), name='all-users'),
    path('all-borrowed-books/', BorrowedBooks.as_view(), name='all-borrowed-books'),
    path("unavailable-books/", UnavailableBooks.as_view(), name="unavailable-books"),
    path("available-books/", AvailableBooks.as_view(), name="available-books"),

]

