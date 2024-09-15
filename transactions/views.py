import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from .models import Transaction, APIKey
from django.contrib import messages
from qrcode import make
from .upi_gateway import create_upi_order  # Import the UPI Gateway utility function
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# API Key Management Dashboard
@login_required
def api_key_dashboard(request):
    """
    Dashboard for users to manage their API key.
    """
    api_key_obj, created = APIKey.objects.get_or_create(user=request.user)
    if request.method == 'POST' and 'regenerate_key' in request.POST:
        api_key_obj.generate_key()
        return redirect('api_key_dashboard')
    
    return render(request, 'dashboard/api_key_dashboard.html', {'api_key': api_key_obj.api_key})

# API Key Deletion
@login_required
def delete_api_key(request):
    """
    Deletes the API key associated with the user.
    """
    api_key_obj = APIKey.objects.get(user=request.user)
    api_key_obj.delete()
    return redirect('api_key_dashboard')

# UPI Callback Handling
@login_required
def upi_callback(request):
    """
    Handles the callback from the UPI Gateway to update transaction status.
    """
    if request.method == 'POST':
        data = request.POST
        transaction_id = data.get('transaction_id')
        status = data.get('status')

        # Update the transaction status based on the callback data
        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
            if status == 'success':
                transaction.status = 'success'
            elif status == 'failed':
                transaction.status = 'failed'
            transaction.save()
            return JsonResponse({'message': 'Transaction status updated'}, status=200)
        except Transaction.DoesNotExist:
            return JsonResponse({'error': 'Transaction not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Transaction Creation
@login_required
def create_transaction(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        # Creating a transaction without needing `upi_reference_id`
        transaction = Transaction.objects.create(
            business=request.user.business,  # Assuming the user is related to a business
            amount=amount,
        )
        return redirect('transaction-detail', transaction_id=transaction.transaction_id)
    
    return render(request, 'transactions/create_transaction.html')

# Transaction Details with QR Code Generation
@login_required
def transaction_detail(request, transaction_id):
    """
    Displays transaction details with QR code and provides options for UPI Gateway or manual verification.
    """
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id, business__user=request.user)
    upi_url = f"upi://pay?pa={transaction.business.upi_id}&pn={transaction.business.name}&am={transaction.amount}&cu=INR"

    # Generate QR code
    qr = make(upi_url)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Base64 encode the image
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Check if using UPI Gateway or manual verification
    if request.method == 'POST':
        if 'gateway' in request.POST:
            # Call UPI Gateway to create the order
            upi_response = create_upi_order(transaction.amount, transaction.business.upi_id)

            if 'error' in upi_response:
                messages.error(request, f"Failed to create UPI order: {upi_response['error']}")
            else:
                # Update the transaction with the UPI gateway response
                transaction.transaction_id = upi_response.get('order_id', 'TXN_GATEWAY_123456')
                transaction.status = 'pending'
                transaction.save()

                # Redirect user to complete payment (or show QR code/URL to pay)
                payment_url = upi_response.get('payment_url')
                if payment_url:
                    return redirect(payment_url)

            messages.success(request, 'Payment has been successfully processed via UPI Gateway.')
            return redirect('dashboard')

        elif 'confirm' in request.POST:
            entered_transaction_id = request.POST.get('transaction_id')

            # Manual verification: Match entered Transaction ID with transaction_id field
            if entered_transaction_id == transaction.transaction_id:
                transaction.status = 'success'
                transaction.save()
                messages.success(request, 'Payment has been verified and marked as successful.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Transaction ID does not match.')

    context = {
        'transaction': transaction,
        'qr_code_base64': qr_code_base64,  # Pass the base64-encoded QR code to the template
    }
    return render(request, 'transactions/transaction_detail.html', context)

# Transactions Overview Page
@login_required
def transactions_overview(request):
    """
    Renders a page that shows all the features and lists all transactions.
    """
    # Fetch all transactions
    transactions = Transaction.objects.filter(business__user=request.user)
    
    # Define the available features for display
    features = [
        'Create a transaction',
        'Generate QR code for payment',
        'Process payments',
        'View transaction details',
        'UPI Callback Handling',
        'API Key Management',
    ]

    context = {
        'transactions': transactions,
        'features': features,
    }
    return render(request, 'transactions/transactions_overview.html', context)