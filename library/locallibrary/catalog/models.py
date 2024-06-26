from django.db import models

# Create your models here.
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.conf import settings

from datetime import date

class Genre(models.Model):
    '''Model representing a book genre'''
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text='Enter a book genre (e.g. Science Fiction, French Poetry etc.)'
    )

    def __str__(self):
        '''String for representing the Model object'''
        return self.name
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message='Genre already exists (case insensitive match)'
            ),
        ]


class Author(models.Model):
    """Model representing the author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access this particular author instance"""
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

class Language(models.Model):
    name = models.CharField(max_length=200, unique=True,help_text='Enter natural language e.g. English, Spanish etc')
    def get_absolute_url(self):
        return reverse('language-detail', args=[str(str.id)])
    
    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message='Language already exists(case insensitive match).'
            )
        ]

class Book(models.Model):
    '''Model representing a book (but not a specific copy of a book)'''
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, null=True)
    '''ForeignKey is used because a book can only have one author but authors can have
    multiple books.
    Author as a string rather than object because it hasn't been declared yet
    in file'''

    summary = models.TextField( max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 characters <a href="www.isbn-internation.org/content/what-isbn">ISBN number</a>')

    ''' ManyToManyField used because genre can contain many books. Books can cover many genres
    Genre class has already been defined so we can specify the object above'''
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL,null=True)
    cover = models.ImageField(upload_to='media',height_field=None, width_field=None,max_length=200 ,null=True, blank=True)

    def __str__(self):
        """String for representing the Model object"""
        return self.title
    
    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book"""
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        '''Function to display genres'''
        return "," .join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'
    
    
import uuid

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. 
    that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across the whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o','On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )

    @property
    def is_due(self):
        return bool( (self.due_back and date.today) > self.due_back)
   
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    


    
