from rest_framework import serializers

from app.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user_id', 'amount', 'currency', 'timestamp']
        read_only_fields = ["user_id"]
