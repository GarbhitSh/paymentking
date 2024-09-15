from django.core.mail import send_mail
from django.conf import settings

def send_confirmation_email(user_email, amount, transaction_id):
    """
    Sends a confirmation email to the user after successful payment.
    """
    subject = 'Payment Successful'
    message = f'Thank you for your payment of INR {amount}. Your transaction ID is {transaction_id}.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
