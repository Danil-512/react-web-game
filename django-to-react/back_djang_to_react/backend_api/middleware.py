class SessionDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("\n=== Request Debug ===")
        print("Headers:", request.headers)
        print("Cookies:", request.COOKIES)
        print("Session Key:", request.session.session_key)

        response = self.get_response(request)

        print("Response Cookies:", response.cookies)
        print("====================\n")
        return response