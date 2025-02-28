# admin/api/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("add-book/", AddBookView.as_view(), name="add-book"),
    path("delete-book/", DeleteBook.as_view(), name="delete-book"),
    path("all-users/", FetchUsers.as_view(), name="receive-user-data"),
    path("all-borrowed-books/", FetchBorrowedBooks.as_view(), name="receive-borrowed-books"),
    path("unavailable-books/", FetchUnavailableBooks.as_view(), name="unavailable-books"),
    path("available-books/", FetchAvailableBooks.as_view(), name="available-books"),
]
