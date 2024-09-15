import requests
from django.conf import settings

def create_upi_order(amount, upi_id):
    """
    Sends a request to the UPI Gateway to create a payment order.
    
    :param amount: The order amount
    :param upi_id: The UPI ID of the customer
    :return: Response from the UPI Gateway API (order details or error)
    """
    url = 'https://api.ekqr.in/api/create_order'
    
    payload = {
        'amount': amount,
        'upi_id': upi_id,
        'merchant_id': settings.UPI_GATEWAY_MERCHANT_ID,
        'callback_url': 'https://yourdomain.com/upi/callback',  # URL to receive payment status updates
    }
    
    headers = {
        'Authorization': f'Bearer {settings.UPI_GATEWAY_API_KEY}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()  # Assuming the API returns JSON
    except requests.RequestException as e:
        return {'error': str(e)}
