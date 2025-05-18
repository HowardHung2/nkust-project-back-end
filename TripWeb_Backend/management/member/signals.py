# management/member/signals.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile
from TripWeb_NFT_Management.createAccount import get_account

@receiver(post_save, sender=User)
def create_user_profile_with_xrpl(sender, instance, created, **kwargs):
    if created:
        wallet = get_account("")  # 建立 XRPL 錢包
        UserProfile.objects.create(
            user=instance,
            xrpl_address=wallet.classic_address,
            xrpl_seed=wallet.seed,
        )
