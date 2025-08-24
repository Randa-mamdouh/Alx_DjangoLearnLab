# CRUD_operations.md
## Create 

# Expected output: <Book: Book object (1)> or similar depending on the primary key
new_book

## Read 
---
from bookshelf.models import Book
new_book = Book.objects.create(title = "1984", author = "George Orwell", publication_year = '1949' )
---

## Update


---
from LibraryProject.models import Book

# Retrieve the book by title
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save() # Save the changes to the database

# Expected output: 'Nineteen Eighty-Four', confirming the title has been updated
book.title # Output: 'Nineteen Eighty-Four'
--- 


## Delete 
book_to_delete.delete()

# Expected output: (1, {'LibraryProjects.book': 1 }), indicating one 'Book' instance was deleted

# Confirm deletiong by retrieveing all books

all_books = Book.objects.all()
all_books # Expected Output: <Query Set[]> if no other books exist, or a list of remaining books
---