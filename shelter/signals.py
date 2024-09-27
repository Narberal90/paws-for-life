from django.db.models.signals import post_save
from django.dispatch import receiver
from shelter.models import Adoption, Animal


@receiver(post_save, sender=Adoption)
def update_animal_status_on_adoption(sender, instance, **kwargs):
    if instance.status == "pending":
        instance.animal.status = Animal.STATUS_CHOICES[2][0]
    elif instance.status == "approved":
        instance.animal.status = Animal.STATUS_CHOICES[1][0]
    elif instance.status == "rejected":
        instance.animal.status = Animal.STATUS_CHOICES[0][0]
    instance.animal.save()
