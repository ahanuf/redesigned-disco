from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_comment_notification(comment_id):
    from .models import Comment
    comment = Comment.objects.get(id=comment_id)
    subject = f"New Comment on: {comment.post.title}"
    message = f"{comment.author} commented: {comment.content}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [comment.post.author.email])
