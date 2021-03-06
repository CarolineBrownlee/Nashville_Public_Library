import sqlite3
from django.shortcuts import render, redirect, reverse
from libraryapp.models import Book
from ..connection import Connection
from libraryapp.models import model_factory
from django.contrib.auth.decorators import login_required

@login_required
def book_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            
            conn.row_factory =  model_factory(Book)
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                b.id,
                b.title,
                b.isbn_number,
                b.author,
                b.year_published,
                b.librarian_id,
                b.location_id
            from libraryapp_book b
            """)

            # When you instruct the sqlite3 package to fetchall(), it takes your SQL string and walks over to the database and executes it. It then takes all of the rows that the database generates, and creates a tuple out of each one. It then puts all of those tuples into a list. (Chapter Documentation, NSS)

            # TUPLE is a collection which is ordered and unchangeable. Allows duplicate members. Parenthesis. (W3 Schools)

            # LIST is a collection which is ordered and changeable. Allows duplicate members. Brackets. (W3 Schools)

            # all_books = []
            all_books = db_cursor.fetchall()

            # commented out code because model_factory(Book) takes care of this
            # for row in dataset:
            #     # creating an instance of a book with Book()
            #     book = Book()
            #     book.id = row['id']
            #     book.title = row['title']
            #     book.isbn_number = row['isbn_number']
            #     book.author = row['author']
            #     book.year_published = row['year_published']
            #     book.librarian_id = row['librarian_id']
            #     book.location_id = row['location_id']

                # all_books.append(book)

        # When a view wants to generate some HTML representations of data, it needs to specify a template to use. [Below], the template variable is holding the path and filename of the template. (Nashville Software School, Ch 3 Documentation)

        template = 'books/list.html'

        # the dictionary 'all_books' has a single property labeled all_books and its value is the list of book objects that the view generates. // The key name is able to be used in a loop in the template.  (Nashville Software School, Ch 3 Documentation)

        context = {
            'all_books': all_books
        }
        # Then the render() method is invoked. That method takes the HTTP request as the first argument, the template to be used as the second argument, and then a dictionary containing the data to be used in the template. (Nashville Software School, Ch 3 Documentation)
        return render(request, template, context)
    
    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO libraryapp_book
            (
                title, author, isbn_number,
                year_published, librarian_id, location_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (form_data['title'], form_data['author'],
            form_data['isbn_number'], form_data['year_published'],
            request.user.librarian.id, form_data["location"]))

        return redirect(reverse('libraryapp:books'))