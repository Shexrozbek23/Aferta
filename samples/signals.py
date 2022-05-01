from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver


# this receiver is executed every-time some data is saved in any table
from samples.models import Sample


@receiver(pre_save, sender=Sample)
def audit_log(sender, instance, **kwargs):
    # code to execute before every model save
    if instance.creator.is_superuser is False:
        instance.creator.region.limit = instance.creator.region.limit - instance.area
        instance.creator.region.save()

