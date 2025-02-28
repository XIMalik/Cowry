# admin/api/views.py
import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

class AddBookView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        book = serializer.save()  

        # Sync with Frontend API
        frontend_api_url = "http://127.0.0.1:8001/add-book/"  # Update if deployed
        data = {
            "id": str(book.id),
            "title": book.title,
            "author": book.author,
            "publisher": book.publisher,
            "category": book.category,
            "available": book.available,
        }

        try:
            response = requests.post(frontend_api_url, json=data)
            if response.status_code == 201:
                print("✅ Book successfully synced to frontend database")
            else:
                print(f"❌ Failed to sync book: {response.text}")
        except Exception as e:
            print(f"⚠️ Error syncing book: {e}")

class DeleteBook(DestroyAPIView):
    queryset = Book.objects.all()

    def delete(self, request, *args, **kwargs):
        title = request.data.get("title")
        try:
            book = Book.objects.get(title=title)
            book.delete()

            frontend_api_url = "http://127.0.0.1:8001/delete-book/"
            data = {"title": str(title)}
            try:
                response = requests.post(frontend_api_url, json=data)
                if response.status_code == 200:
                    return Response({"message": "Book deleted successfully"}, status=200)
                else:
                    return Response({"message": "Book deleted successfully", "warning": "Failed to sync deletion with frontend"}, status=200)
            except Exception as e:
                print(f"⚠️ Error syncing book deletion: {e}")
                return Response({"message": "Book deleted successfully", "warning": "Failed to sync deletion with frontend"}, status=200)

        except Book.DoesNotExist:
            return Response({"message": "Book not found"}, status=404)
        
class FetchUsers(APIView):
    def get(self, request):
        frontend_url = "http://127.0.0.1:8001/all-users/"  

        try:
            response = requests.get(frontend_url)  # Fetch user data
            if response.status_code == 200:
                user_data = response.json()
                print("✅ Successfully fetched user data:", user_data)
                return Response(user_data, status=status.HTTP_200_OK)
            else:
                print(f"❌ Failed to fetch data: {response.text}")
                return Response({"error": "Failed to fetch user data"}, status=response.status_code)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class FetchBorrowedBooks(APIView):
    def get(self, request):
        frontend_url = "http://127.0.0.1:8001/all-borrowed-books/"  

        try:
            response = requests.get(frontend_url)  # Fetch user data
            if response.status_code == 200:
                user_data = response.json()
                print("✅ Successfully fetched borrowed books:", user_data)
                return Response(user_data, status=status.HTTP_200_OK)
            else:
                print(f"❌ Failed to fetch data: {response.text}")
                return Response({"error": "Failed to fetch data"}, status=response.status_code)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class FetchUnavailableBooks(APIView):
    def get(self, request):
        frontend_url = "http://127.0.0.1:8001/unavailable-books/"

        try:
            response = requests.get(frontend_url)  # Fetch borrowed books
            if response.status_code == 200:
                borrowed_books = response.json()
                print("✅ Successfully fetched borrowed books:", borrowed_books)
                return Response(borrowed_books, status=status.HTTP_200_OK)
            else:
                print(f"❌ Failed to fetch borrowed books: {response.text}")
                return Response({"error": "Failed to fetch borrowed books"}, status=response.status_code)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class FetchAvailableBooks(APIView):
    def get(self, request):
        frontend_url = "http://127.0.0.1:8001/available-books/"

        try:
            response = requests.get(frontend_url)  # Fetch borrowed books
            if response.status_code == 200:
                borrowed_books = response.json()
                print("✅ Successfully fetched available books:", borrowed_books)
                return Response(borrowed_books, status=status.HTTP_200_OK)
            else:
                print(f"❌ Failed to fetch available books: {response.text}")
                return Response({"error": "Failed to fetch borrowed books"}, status=response.status_code)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
