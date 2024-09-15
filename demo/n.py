import requests
import json

# Define the API endpoint for processing payments
api_url = "http://127.0.0.1:8000/transactions/api/process_payment/"

# Set your API token if the API requires authentication
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI2MzQ2NzM5LCJpYXQiOjE3MjYzNDY0MzksImp0aSI6IjNmODhjMjBkMjA2OTRiOTM4NTRmMjE1YzdlNDY3OGVhIiwidXNlcl9pZCI6MX0.LOgpRsyt1Bn3rWpPJ3prC2VmJaLNvwAn-eYN010gUHE"  # Replace this with your actual JWT token

# Headers for the request (including Authorization)
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_token}"  # Add JWT token for authentication
}

# Define the data for the API request
data = {
    "amount": "500.00",  # Amount in INR
    "upi_id": "customer@upi",  # The UPI ID of the customer
    "callback_url": "https://example.com/callback"  # The callback URL
}

# Make the POST request to the API
try:
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    
    # Check if the request was successful (status code 201)
    if response.status_code == 201:
        print("Payment order created successfully!")
        print("Response:", response.json())
    else:
        print(f"Failed to create payment order. Status Code: {response.status_code}")
        print("Response:", response.json())

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
