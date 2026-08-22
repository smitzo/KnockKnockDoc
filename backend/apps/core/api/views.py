from django.conf import settings
from django.db import connection
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView


class HealthView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "health"

    def get(self, request):
        database_status = "unavailable"
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            database_status = "ready"
        except Exception:  # The response deliberately omits internal database errors.
            pass

        status_code = 200 if database_status == "ready" else 503
        return Response(
            {
                "service": "knocknockdoc-api",
                "status": "ready" if status_code == 200 else "degraded",
                "database": database_status,
                "version": settings.APP_VERSION,
                "prototype_mode": settings.PROTOTYPE_MODE,
                "data_policy": "synthetic-only" if settings.PROTOTYPE_MODE else "configured",
            },
            status=status_code,
        )
