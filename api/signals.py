# # admin/signals.py
# import requests
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Book

# @receiver(post_save, sender=Book)
# def sync_book_to_frontend(sender, instance, created, **kwargs):
#     if created:
#         frontend_api_url = "http://127.0.0.1:8000/add-book/"
#         data = {
#             "id": str(instance.id),
#             "title": instance.title,
#             "author": instance.author,
#             "publisher": instance.publisher,
#             "category": instance.category,
#             "available": instance.available,
#         }
#         try:
#             response = requests.post(frontend_api_url, json=data)
#             if response.status_code == 201:
#                 print("✅ Book successfully synced to frontend database")
#             else:
#                 print(f"❌ Failed to sync book: {response.text}")
#         except Exception as e:
#             print(f"⚠️ Error syncing book: {e}")
