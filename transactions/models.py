# transactions/models.py
from django.db import models
from businesses.models import Business

from django.db import models
from django.contrib.auth.models import User
import uuid
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('success', 'Success'),
    ('failed', 'Failed'),
]

class APIKey(models.Model):
    """
    Stores API keys for users, used to access the QR code payment API.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)

    def generate_key(self):
        """
        Generates a new API key.
        """
        self.api_key = uuid.uuid4().hex
        self.save()

    def __str__(self):
        return f"{self.user.username}'s API Key"

class Transaction(models.Model):
    business = models.ForeignKey('businesses.Business', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4().hex)  # Use this field
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"