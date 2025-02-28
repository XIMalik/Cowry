from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
import uuid
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
    
class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30, null=False, blank=False)
    author = models.CharField(max_length=30, null=False, blank=False)
    publisher = models.CharField(max_length=30, null=False, blank=False)
    category = models.CharField(max_length=30, null=False, blank=False)
    available = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

class BorrowedBook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowed_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowed_books")
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()

    class Meta:
        verbose_name = "Borrowed Book"
        verbose_name_plural = "Borrowed Books"

    def save(self, *args, **kwargs):
        if not self.return_date:
            self.return_date = now() + timedelta(days=14) 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title} until {self.return_date}"    




