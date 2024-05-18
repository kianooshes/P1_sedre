from django.urls import path
from . import views

app_name = "bookselling_api"

urlpatterns = [
    path("books/", views.BookList.as_view()),
    path(
        "books/purchase/<int:book_id>/",
        views.PurchaseBook.as_view(),
        name="purchase_book",
    ),
    path("books/user/", views.UserBookList.as_view()),
    path(
        "books/return/<int:user_book_id>/",
        views.ReturnBook.as_view(),
        name="return_book",
    ),
    path("changebalance/", views.UpdateMultipleUserBalances.as_view()),
]
