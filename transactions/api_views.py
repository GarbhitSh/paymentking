from django.http import JsonResponse
import base64
from io import BytesIO
from qrcode import make
from .models import APIKey  # Ensure that APIKey and related models are imported

from .models import Transaction

def validate_api_key(request):
    """
    Validates the provided API key in the request headers.
    """
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return None, JsonResponse({'error': 'API key is missing'}, status=403)

    try:
        api_key_obj = APIKey.objects.get(api_key=api_key)
        return api_key_obj, None
    except APIKey.DoesNotExist:
        return None, JsonResponse({'error': 'Invalid API key'}, status=403)

def generate_qr_code_api(request):
    """
    API endpoint to generate a QR code for UPI payment.
    Requires a valid API key in the request headers.
    """
    api_key_obj, error_response = validate_api_key(request)
    if error_response:
        return error_response
    
    amount = request.GET.get('amount')
    if not amount:
        return JsonResponse({'error': 'Amount is required'}, status=400)

    upi_id = api_key_obj.user.business.upi_id  # Assuming Business model is linked to the user
    upi_url = f"upi://pay?pa={upi_id}&pn={api_key_obj.user.business.name}&am={amount}&cu=INR"

    # Generate QR code
    qr = make(upi_url)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    buffer.seek(0)
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    return JsonResponse({'qr_code_base64': qr_code_base64, 'upi_url': upi_url})
def process_payment(request):
    """
    API endpoint to process a payment. 
    It validates the transaction and marks it as complete.
    """
    transaction_id = request.POST.get('transaction_id')
    status = request.POST.get('status')  # 'success' or 'failed'

    if not transaction_id or not status:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    # Fetch the transaction
    try:
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except Transaction.DoesNotExist:
        return JsonResponse({'error': 'Transaction not found'}, status=404)

    # Update transaction status
    transaction.status = status
    transaction.save()

    return JsonResponse({'message': 'Payment processed successfully', 'status': transaction.status})
