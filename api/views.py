from django.shortcuts import render
from .models import *
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.decorators import api_view
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import CustomUser, Book
import requests

# Create your views here.

class Register(CreateAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        password = request.data.get("password")

        if not email or not first_name or not last_name or not password:
            return Response(
                {"error": "All fields are required"}, status=HTTP_400_BAD_REQUEST
            )
        
        try:
            user = CustomUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )

            return Response(
                {"message": "Library user created successfully"}, status=HTTP_201_CREATED
            )

        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Book added successfully"}, status=201)
    return Response(serializer.errors, status=400)

@api_view(["POST"])
def delete_book(request):
    title = request.data.get("title")
    if not title:
        return Response({"message": "Book title is required"}, status=400)

    book = get_object_or_404(Book, title=title)
    book.delete()
    return Response({"message": "Book deleted successfully"}, status=200)

class ListBooks(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class GetSingleBook(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, book_id, *args, **kwargs):
        book = get_object_or_404(Book, pk=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class FilterBooks(ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        publisher = self.request.query_params.get("publisher")
        category = self.request.query_params.get("category")

        if publisher:
            queryset = queryset.filter(publisher__iexact=publisher) 
        if category:
            queryset = queryset.filter(category__iexact=category)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No books found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BorrowBook(CreateAPIView):

    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book_id")
        days = request.data.get("days", 14) 

        user = request.user

        print ("this is user", user)

        if not book_id:
            return Response({"message": "Book ID is required"}, status=400)

        book = get_object_or_404(Book, id=book_id)

        if not book.available:
            return Response({"message": "This book is currently unavailable"}, status=400)

        # Calculate return date
        return_date = now() + timedelta(days=int(days))

        # Create BorrowedBook entry
        BorrowedBook.objects.create(
            user=request.user,
            book=book,
            return_date=return_date
        )

        # Mark book as unavailable
        book.available = False
        book.save()

        return Response({"message": "Book borrowed successfully", "return_date": return_date}, status=201)

class AllUsers(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class BorrowedBooks(ListAPIView):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer

class UnavailableBooks(ListAPIView):

    queryset = BorrowedBook.objects.all()
    serializer_class = UnavailableBookSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No books currently borrowed"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AvailableBooks(ListAPIView):
    
    queryset = Book.objects.filter(available=True)
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No books currently available"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)