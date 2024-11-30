from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import Transaction


class StatsViewTest(APITestCase):

    def setUp(self):
        Transaction.objects.create(amount=100.0, currency='USD')
        Transaction.objects.create(amount=200.0, currency='USD')
        Transaction.objects.create(amount=150.0, currency='USD')

    def test_get_stats(self):
        url = reverse('transaction_stats')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_transactions'], 3)
        self.assertEqual(response.data['total_amount'], 450.0)
        self.assertEqual(response.data['currency'], 'USD')