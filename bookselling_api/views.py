from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer, UserBookSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from bookselling.models import Book, UserBook
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from accounts.models import User


class BookList(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "books/booklist_api.html"
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(owner=None)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"books": serializer.data})


class PurchaseBook(CreateAPIView):
    serializer_class = UserBookSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "book_id"

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        book_id = kwargs.get(self.lookup_url_kwarg)
        try:
            book = Book.objects.select_for_update().get(id=book_id, owner=None)
            user = request.user

            user_balance = user.balance
            book_price = book.price

            if user_balance < book_price:
                return Response(
                    {"error": "Insufficient balance"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.balance -= book_price
            user.save()

            serializer = self.get_serializer(data={"user": user.id, "book": book_id})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            book.owner = user
            book.save()
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ReturnBook(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "user_book_id"

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        user_book_id = kwargs.get(self.lookup_url_kwarg)
        try:
            user_book = UserBook.objects.select_for_update().get(id=user_book_id)
            book = user_book.book
            user = request.user

            user.balance += book.price
            user.save()

            book.owner = None
            book.save()
            user_book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserBook.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserBookList(ListAPIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "userbooks/userbooks_api.html"
    serializer_class = UserBookSerializer

    def get_queryset(self):
        return UserBook.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"user_books": serializer.data})


class UpdateMultipleUserBalances(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        changes = request.data.get("changes", [])
        if not isinstance(changes, list):
            return Response(
                {"error": "Invalid format for changes."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for change in changes:
            username = change.get("username")
            amount = change.get("amount")

            if username is None or amount is None:
                return Response(
                    {"error": "Username or amount is missing in changes."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.filter(username=username).first()
            if user is None:
                return Response(
                    {"error": f"User with username {username} not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            user.balance += amount
            user.save()

        return Response(
            {"message": "User balances updated successfully."},
            status=status.HTTP_200_OK,
        )
