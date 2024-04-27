from django.urls import path
from. import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('', views.book_list, name='book_list'),
    path('purchase_book/<int:book_id>/', views.purchase_book, name='purchase_book'),
    path('user_book_list/', views.user_book_list, name='user_book_list'),
    path('return_book/<int:user_book_id>/', views.return_book, name='return_book'),
    path('logout/', views.logout_view, name='logout'),
]