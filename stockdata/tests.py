from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from usermanagement.models import CustomUser as User
from .models import General, Note
from unittest.mock import patch


class StockDataTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            is_active=True
        )
        self.general = General.objects.create(
            code="AAPL",
            name="Apple Inc.",
            uid="apple-uid"
        )
        self.note = Note.objects.create(
            user=self.user,
            stock=self.general,
            content="This is a test note."
        )

    @patch(
        'rest_framework.authentication.SessionAuthentication.enforce_csrf',
        return_value=None
    )
    def test_stock_detail_view(self, _):
        url = reverse('stock_detail', args=['apple-uid'])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['uid'], 'apple-uid')

    @patch(
        'rest_framework.authentication.SessionAuthentication.enforce_csrf',
        return_value=None
    )
    def test_toggle_follow_stock(self, _):
        url = reverse('toggle_follow_stock', args=['apple-uid'])
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch(
        'rest_framework.authentication.SessionAuthentication.enforce_csrf',
        return_value=None
    )
    def test_note_list_create_view(self, _):
        url = reverse('note-list-create')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            'content': 'A new test note.',
            'stock': self.general.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch(
        'rest_framework.authentication.SessionAuthentication.enforce_csrf',
        return_value=None
    )
    def test_note_detail_view(self, _):
        url = reverse('note-detail', args=[self.note.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            'content': 'Updated test note.',
            'stock': self.general.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch(
        'rest_framework.authentication.SessionAuthentication.enforce_csrf',
        return_value=None
    )
    def test_followed_stocks_view(self, _):
        url = reverse('followed-stocks')
        self.general.followers.add(self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch(
        'rest_framework.authentication.SessionAuthentication.enforce_csrf',
        return_value=None
    )
    def test_stock_search_view(self, _):
        url = reverse('stock-search') + '?query=Apple'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch(
        'rest_framework.authentication.SessionAuthentication.enforce_csrf',
        return_value=None
    )
    def test_dividend_data_list_view(self, _):
        url = reverse('dividend-data-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
