from rest_framework import serializers
from .models import *

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook