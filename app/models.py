from django.db import models


class Transaction(models.Model):
    user_id = models.IntegerField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.user_id:
            last_user_id = Transaction.objects.last()
            self.user_id = (last_user_id.user_id + 1) if last_user_id else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction {self.id} by User {self.user_id}"
