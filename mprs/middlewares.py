from rest_framework.authtoken.models import Token

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_anonymous and 'Authorization' in request.headers:
            key = request.headers['Authorization'].split()[1]
            request.user = Token.objects.get(key=key).user
        response = self.get_response(request)
        return response