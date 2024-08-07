from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from catalog.forms import RenewBookModelForm
from django.contrib.auth.decorators import login_required, permission_required
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
    # number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'genre_count_word': genre_count_word,
        'books_count_word': books_count_word,
        'num_visits': num_visits,

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

# LoginRequiredMixin makes it to where the view is only able to be seen if the user is logged in
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    # reimplementing queryset to restrict our query to just BookInstance objects for the current user
    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        )

class AllBorrowedBooksList(LoginRequiredMixin, generic.ListView):
    template_name = 'catalog/all_borrowed.html'
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    
    def get_queryset(self):
        return (
            BookInstance.objects.all()
        )


@login_required  # user needs to be logged in
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a speciric BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    #If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)


        # Check if the form is valid:
        # this also calls our forms clean_renewal_date() function
        if form.is_valid():
            # Process the data in form.cleaned_data as required (here we jsut write to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()


            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))
    
    # If this is a GET (or any other method create the default form.)
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = { 'form': form, 'book_instance': book_instance}

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    # initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    # not recommended (potential security issues if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_author'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse('author-delete', kwargs={"pk": self.object.pk})
            )


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = "__all__"
    permission_required = "catalog.add_book"


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = "__all__"
    permission_required = "catalog.change_book"


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy("books")
    permission_required = "catalog.delete_book"

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse('book-delete', kwargs={"pk": self.object.pk}))