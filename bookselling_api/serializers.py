from rest_framework import serializers
from bookselling.models import Book , UserBook 

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBook
        fields = "__all__"

        