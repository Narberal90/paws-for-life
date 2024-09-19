from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Adoption, Animal

@receiver(post_save, sender=Adoption)
def update_animal_status_on_adoption(sender, instance, **kwargs):
    if instance.status == "pending":
        instance.animal.status = "pending"
    elif instance.status == "approved":
        instance.animal.status = "adopted"
    elif instance.status == "rejected":
        instance.animal.status = "available"
    instance.animal.save()