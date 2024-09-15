from django.core.management.base import BaseCommand
from transactions.models import Transaction
import uuid

class Command(BaseCommand):
    help = 'Fix transactions by assigning a unique transaction_id to any record that is missing one.'

    def handle(self, *args, **kwargs):
        # Fetch transactions where transaction_id is null
        transactions_without_id = Transaction.objects.filter(transaction_id__isnull=True)
        self.stdout.write(f'Found {transactions_without_id.count()} transactions without transaction_id')

        for transaction in transactions_without_id:
            # Generate a unique transaction_id
            transaction.transaction_id = uuid.uuid4().hex
            transaction.save()
            self.stdout.write(f'Updated transaction {transaction.id} with transaction_id {transaction.transaction_id}')

        self.stdout.write('Fix completed.')
