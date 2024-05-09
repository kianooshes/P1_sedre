from rest_framework import serializers
from bookselling.models import Book, UserBook
from accounts.models import User


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBook
        fields = "__all__"


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserBalanceUpdateSerializer(serializers.Serializer):
    changes = serializers.ListField(child=serializers.DictField())

    def validate_changes(self, value):
        if not all("username" in item and "amount" in item for item in value):
            raise serializers.ValidationError(
                "Each change entry should have 'username' and 'amount'."
            )
        return value
