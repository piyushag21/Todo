# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import User

# @receiver(post_save, sender=User)
# def set_domain_admin(sender, instance, created, **kwargs):
#     if created and not User.objects.filter(domain=instance.domain, is_domain_admin=True).exists():
#         instance.is_domain_admin = True
#         instance.save()
