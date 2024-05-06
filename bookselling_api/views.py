from django.shortcuts import render
from bookselling.models import Book , UserBook 
from rest_framework.generics import ListCreateAPIView
from .serializers import BookSerializer , UserBookSerializer

class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class UserBookList(ListCreateAPIView):
    queryset = UserBook.objects.all()
    serializer_class = UserBookSerializer


