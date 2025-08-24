from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Book
from .urls import urlpatterns

# Create your tests here.

# This Python class contains test cases for creating, retrieving, updating, and deleting books using
# Django REST framework API testing.
class BookAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2021
        }
        self.create_url = reverse('create')  
        self.detail_url = reverse('book_detail', args=[1])
        self.update_url = reverse('update', args=[1])
        self.delete_url = reverse('delete', args=[1])

    def test_create_book(self):
        response = self.client.post(self.create_url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.book_data['title'])
        self.assertEqual(Book.objects.count(), 1)
        
    def test_get_books(self):
        # Create a book
        Book.objects.create(title='Test Book', author='Test Author', publication_year=2021)

        # Retrieve books
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Book')
        
    def test_update_book(self):
        # Create a book
        book = Book.objects.create(title='Test Book', author='Test Author', publication_year=2021)
        update_url = reverse('update', args=[book.id])  # Assuming 'detail' is the name of the detail URL

        # Update the book
        updated_data = {'title': 'Updated Title'}
        response = self.client.patch(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
    def test_delete_book(self):
        # Create a book
        book = Book.objects.create(title='Test Book', author='Test Author', publication_year=2021)
        delete_url = reverse('delete', args=[book.id])

        # Delete the book
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)