class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        origin = request.headers.get('Origin')

        if origin in ["http://localhost:5173", "http://127.0.0.1:5173"]:
            response['Access-Control-Allow-Origin'] = origin
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Expose-Headers'] = 'Set-Cookie'
            response['Access-Control-Allow-Headers'] = 'Content-Type, X-CSRFToken'
            response['Vary'] = 'Origin'

        return response