from django.contrib.auth import get_user_model
from django.db import connection
from django.utils import timezone
from django.core.mail import send_mail

# pyright: reportMissingImports=false
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

class CheckV1View(APIView):
    """
    GET /api/v1/
    Attempts a simple version return.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs): # <- accepts version and any other kwargs
        try:
            return Response({
                "message": "API v1 enabled.",
                "status": True,
                "datetime": timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
        except Exception as exc:
            return Response({
                "message": "API v1 is disabled.",
                "status": False,
                "error": str(exc),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckDatabaseView(APIView):
    """
    GET /api/v1/test/database
    Attempts a simple DB query (SELECT 1) and returns status.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs): # <- accepts version and any other kwargs
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                row = cursor.fetchone()
            return Response({
                "message": "API successfully connect to database.",
                "connection": True,
                "result": row,
                "datetime": timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
        except Exception as exc:
            return Response({
                "message": "API failed to connect to database.",
                "connection": False,
                "error": str(exc),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckSendMailView(APIView):
    """
    POST /api/v1/test/send-mail
    Sends a test email via configured SMTP backend (MailHog).
    JSON body optional: { "to": "recipient@example.com", "subject": "...", "body": "..." }
    If not provided, defaults are used (TEST_MAIL_TO env or no-reply@example.com).
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        to = request.data.get("to") or None
        subject = request.data.get("subject") or "Test email from Django app"
        body = request.data.get("body") or f"Test email sent at {timezone.now().isoformat()}"

        # default recipient fallback from env
        from django.conf import settings

        default_recipient = os_recipient = getattr(settings, "TEST_MAIL_TO", None)
        if not to:
            to = os_recipient or request.data.get("to") or ["test@example.com"]

        # ensure list
        if isinstance(to, str):
            recipients = [to]
        else:
            recipients = list(to)

        try:
            sent = send_mail(
                subject,
                body,
                getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
                recipients,
                fail_silently=False,
            )
            return Response({
                "message": "Test email has been sent.",
                "sent": True,
                "sent_count": sent,
                "recipients": recipients,
                "datetime": timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
        except Exception as exc:
            return Response({
                "message": "Test email failed.",
                "sent": False,
                "error": str(exc),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
