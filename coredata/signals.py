from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver


# this receiver is executed every-time some data is saved in any table
from coredata.models import Region, SamplesSniffer


@receiver(pre_save, sender=Region)
def audit_log(sender, instance, **kwargs):
    # code to execute before every model save
    pass
    log = SamplesSniffer.objects.create(limit=instance.limit, name_uz=instance.name_uz)