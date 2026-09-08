from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from .models import Message, OfflineNotification


@shared_task
def send_push_notification(user_id, message_data):
    OfflineNotification.objects.create(
        user_id=user_id,
        message_id=message_data.get('id'),
        title=message_data.get('sender'),
        body=message_data.get('content'),
        timestamp=timezone.now(),
    )

    send_mail(
        subject=f"New message from {message_data.get('sender')}",
        message=message_data.get('content'),
        from_email='no-reply@yourapp.com',
        recipient_list=[message_data.get('user_email')],
        fail_silently=True,
    )


@shared_task
def delete_ephemeral(message_id):
    """Was referenced by consumers.py but never defined. Added here."""
    Message.objects.filter(pk=message_id).delete()