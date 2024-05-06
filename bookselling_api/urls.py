from django.urls import path,include
from .views import BookList,UserBookList

app_name = "api"

urlpatterns = [
    path("booklist/",BookList.as_view(),name="booklist"),
    path("userbooklist/",UserBookList.as_view(),name="userbooklist"),
]

