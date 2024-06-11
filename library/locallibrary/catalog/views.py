from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from catalog.forms import SignUpUserForm

class RegisterUserView(generic.CreateView):
    form_class=SignUpUserForm
    success_url=reverse_lazy('login')
    template_name='registration/signup.html'
    

def index(request):

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.all().count()

    context= {
        'num_books': num_books,
        'num_authors': num_authors,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available
    }

    return render(request, 'catalog/index.html', context=context)

class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author