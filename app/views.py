import requests
from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionView(APIView):

    def get_exchange_rate(self, from_currency, to_currency):
        """
        Fetches the exchange rate from ExchangeRate-API v6 and returns the conversion rate.
        """
        url = f"https://v6.exchangerate-api.com/v6/1ffdb94b9f26b0f1c6f30c35/latest/{from_currency}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if 'conversion_rates' in data:
                if to_currency in data['conversion_rates']:
                    return data['conversion_rates'][to_currency]
                else:
                    print(f"Error: {to_currency} not found in conversion rates.")
                    return None
            else:
                print("Error: 'conversion_rates' not found in the API response.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchange rate: {e}")
            return None

    def post(self, request):
        data = request.data

        try:
            amount = float(data["amount"])
        except ValueError:
            return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)

        if data.get("currency") == "EUR":
            exchange_rate = self.get_exchange_rate("EUR", "USD")
            if exchange_rate is not None:

                converted_amount = round(amount * exchange_rate, 2)
                data["amount"] = converted_amount
                data["currency"] = "USD"
            else:
                return Response({"error": "Failed to fetch exchange rate"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TransactionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatsView(APIView):
    def get(self, request):
        total_transactions = Transaction.objects.count()
        total_amount = Transaction.objects.aggregate(Sum('amount'))['amount__sum'] or 0

        currency = "USD"

        return Response({
            "total_transactions": total_transactions,
            "total_amount": total_amount,
            "currency": currency
        })
