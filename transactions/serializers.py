from rest_framework import serializers

class PaymentRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    upi_id = serializers.CharField(max_length=100)
    callback_url = serializers.URLField()
