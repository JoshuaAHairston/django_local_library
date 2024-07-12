from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register the Admin classes for Book using the decorator


class BooksInstanceInline(admin.TabularInline):
    """Allows for book instances to be seen related to a book in the book detail view"""
    model = BookInstance
    # this allows for only the instances made for the book to be shown
    # and no spare empty book instances
    extra = 0


class BookInline(admin.TabularInline):
    """Allows for books to be seen related to a author in the author's detail view"""
    model = Book
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # allows people on the admin site to filter book instances by these two filters
    list_filter = ('status', 'due_back')

    list_display = ('book', 'status', 'due_back', 'id')
    # changes the book instance detail view by giving the status
    # and avalibility fields a title
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    # displays more fields than just the authors first name and last name
    # on the admin page (overrides the default __str__() text)
    list_display = ('last_name', 'first_name', 'date_of_birth',
                    'date_of_death')
    # changes the author detail view, so now date of birth and death are aligned
    # horizontally
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    inlines = [BookInline]


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

# Register your models here.
# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)
