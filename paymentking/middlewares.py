from django.http import JsonResponse
from transactions.models import APIKey

class APIKeyMiddleware:
    """
    Middleware to check for API key in requests to the API.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            api_key = request.headers.get('X-API-KEY')
            if not api_key:
                return JsonResponse({'error': 'API key is missing'}, status=403)

            try:
                APIKey.objects.get(api_key=api_key)
            except APIKey.DoesNotExist:
                return JsonResponse({'error': 'Invalid API key'}, status=403)

        response = self.get_response(request)
        return response
