import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def prototype_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return response

    view_name = context.get("view", type("Unknown", (), {})).__class__.__name__
    logger.exception("Unhandled API exception in view=%s", view_name)
    return Response(
        {"detail": "The request could not be completed. Please retry or contact the prototype team."},
        status=500,
    )
