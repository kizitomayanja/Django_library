from django.contrib import admin
from .models import Author, Book, Language, BookInstance, Genre

# Register your models here.

class BookInline(admin.TabularInline):
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BookInstanceInline]
#admin.site.register(Genre)
#admin.site.register(Book)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'status', 'borrower', 'due_back', 'id']
    list_filter = ['status', 'due_back']

    fieldsets = (
        (
            (None, {
                'fields': ('book','imprint', 'id')
            }),
            ('Availability', {
                'fields':('status', 'due_back', 'borrower')
            })
        )
    )


#admin.site.register(BookInstance)
admin.site.register(Language)