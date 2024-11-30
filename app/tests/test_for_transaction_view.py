from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TransactionViewTest(APITestCase):

    def test_create_transaction_eur_to_usd(self):
        url = reverse('create_transaction')
        data = {
            "amount": "100.0",
            "currency": "EUR"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['currency'], 'USD')
        self.assertGreater(float(response.data['amount']), 100.0)

    def test_create_transaction_usd(self):
        url = reverse('create_transaction')
        data = {
            "amount": "100.0",
            "currency": "USD"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['currency'], 'USD')
        self.assertEqual(float(response.data['amount']), 100.0)