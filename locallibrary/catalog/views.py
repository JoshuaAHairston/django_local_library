from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic

# Create your views here.


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()


    # Available books (status = 'a')
    num_instances_available = \
        BookInstance.objects.filter(status__exact='a').count()

    # The 'all' is implied by default.

    num_authors = Author.objects.count()
    # filter(field_name__match_type)
    genre_count_word = Genre.objects.filter(name__contains='Fantasy').count()
    books_count_word = Book.objects.filter(title__contains='The').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'genre_count_word': genre_count_word,
        'books_count_word': books_count_word,
    }

    # Render the HTML template index.html with the data in the context variable

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    # making generic class based views makes things way easier than making functions for
    # the views because the generic view already implements most of the functionality we want.
    # here, making model = book queries the database to get all records for the specified model
    # so in this instance it is book
    model = Book
    paginate_by = 2


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author
