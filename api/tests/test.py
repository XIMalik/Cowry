from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Book, BorrowedBook
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()

class LibraryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create a test user
        self.user = User.objects.create_user(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="password123"
        )
        
        self.client.force_authenticate(user=self.user)
        
        # Create a test book
        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            publisher="Publisher",
            category="Fiction",
            available=True
        )

    def test_register_user(self):
        url = reverse("register")  # Ensure you have this view registered in urls.py
        data = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "securepassword"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_book(self):
        url = reverse("add_book")
        data = {
            "title": "New Book",
            "author": "New Author",
            "publisher": "New Publisher",
            "category": "Sci-Fi"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_delete_book(self):
        url = reverse("delete_book")
        data = {"title": "Test Book"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.count(), 0)

    def test_borrow_book(self):
        url = reverse("borrow_book")
        data = {"book_id": str(self.book.id), "days": 7}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertFalse(self.book.available)
        self.assertEqual(BorrowedBook.objects.count(), 1)

    def test_list_available_books(self):
        url = reverse("available_books")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_list_borrowed_books(self):
        BorrowedBook.objects.create(
            user=self.user,
            book=self.book,
            return_date=now() + timedelta(days=14)
        )
        url = reverse("borrowed_books")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_books(self):
        url = reverse("filter_books") + "?category=Fiction"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
