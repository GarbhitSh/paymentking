# businesses/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm, BusinessForm
from django.contrib.auth.decorators import login_required
from .models import Business
from transactions.models import Transaction
from django.shortcuts import render, redirect
from rest_framework_api_key.models import APIKey
from django.contrib import messages


from rest_framework_api_key.models import APIKey
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        business_form = BusinessForm(request.POST)
        if user_form.is_valid() and business_form.is_valid():
            user = user_form.save()
            business = business_form.save(commit=False)
            business.user = user
            business.save()
            login(request, user)
            return redirect('dashboard')
    else:
        user_form = UserRegisterForm()
        business_form = BusinessForm()
    context = {
        'user_form': user_form,
        'business_form': business_form
    }
    return render(request, 'businesses/register.html', context)

@login_required
def dashboard(request):
    business = Business.objects.get(user=request.user)
    transactions = Transaction.objects.filter(business=business)
    return render(request, 'businesses/dashboard.html', {'business': business, 'transactions': transactions})



def api_key_list(request):
    """
    Display all API keys for the logged-in user.
    """
    api_keys = APIKey.objects.filter(created_by=request.user)
    return render(request, 'transactions/api_key_list.html', {'api_keys': api_keys})

def generate_api_key(request):
    """
    Generate a new API key for the logged-in user.
    """
    if request.method == 'POST':
        name = request.POST.get('name')

        if not name:
            messages.error(request, 'API Key name is required.')
            return redirect('api-key-list')

        api_key, key = APIKey.objects.create_key(name=name, created_by=request.user)

        # Show the key to the user; they need to store it somewhere
        messages.success(request, f'API Key generated successfully: {key}')
        return redirect('api-key-list')

    return render(request, 'transactions/generate_api_key.html')

def revoke_api_key(request, api_key_id):
    """
    Revoke (delete) an API key.
    """
    api_key = APIKey.objects.filter(id=api_key_id, created_by=request.user).first()

    if not api_key:
        messages.error(request, 'API Key not found or you don’t have permission to revoke it.')
        return redirect('api-key-list')

    api_key.delete()
    messages.success(request, 'API Key revoked successfully.')
    return redirect('api-key-list')    