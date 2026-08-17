from django.conf import settings


class PrototypeBoundaryMiddleware:
    """Make the anonymous synthetic-data boundary visible on every API response."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Content-Type-Options"] = "nosniff"
        response["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=()"
        if request.path.startswith("/api/"):
            response["Cache-Control"] = "no-store"
            response["X-Prototype-Mode"] = "synthetic-only" if settings.PROTOTYPE_MODE else "off"
        return response
