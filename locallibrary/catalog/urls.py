from django.urls import path
from . import views

# Use the name attribute here for your static html when linking with urls.
urlpatterns = [
    # look in the base_generic html template to see how the name attribute here is being
    # used properly. 
    # here is a view as a function
    path('', views.index, name='index'),
    # here is a view as a class
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.AllBorrowedBooksList.as_view(), name='all-borrowed'),

]
