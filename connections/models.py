from django.db import models
from django.contrib.auth.models import User


class Invitation(models.Model):
    INVITATION_TYPES = [
        ('send', 'Send'),
        ('accept', 'Accept'),
        ('reject', 'Reject'),
    ]
    from_user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='sent_invitations')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='received_invitations')
    invitation_type = models.CharField(
        max_length=10,
        choices=INVITATION_TYPES,
        default='send',
    )
