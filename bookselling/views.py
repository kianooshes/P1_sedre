from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from.models import Book, UserBook
from django.contrib.auth import logout
from django.contrib.auth.models import User

@login_required
def book_list(request):
    books = Book.objects.filter(owner=None)
    return render(request, 'book_list.html', {'books': books})

@login_required
def purchase_book(request, book_id):
    book = Book.objects.get(id=book_id, owner=None)
    user = User.objects.get(id=request.user.id)
    user_book = UserBook.objects.create(user=user, book=book)
    user_book.save()
    book.owner = request.user
    book.save()
    return redirect('book_list')

@login_required
def user_book_list(request):
    user = User.objects.get(id=request.user.id)
    user_books = UserBook.objects.filter(user=user)
    print(user_books)
    return render(request, 'user_book_list.html', {'user_books': user_books})

@login_required
def return_book(request, user_book_id):
    user_book = UserBook.objects.get(id=user_book_id)
    book = user_book.book
    book.owner = None
    user_book.delete()
    book.save()
    return redirect('user_book_list')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


