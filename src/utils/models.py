from django.db import models
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _


# ===========================================================================
# =========================== Singleton Model ===============================
# ===========================================================================
class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        if not created:
            obj.set_cache()
        return cache.get(cls.__name__)


# ===========================================================================
# =========================== Kavenegar Config Model ========================
# ===========================================================================
class KavenegarConfig(SingletonModel):
    title = models.CharField(_('Kavenegar Config Name'), max_length=200, default='No Name')
    api = models.CharField(_('Kavenegar API Key'), max_length=200, blank=True, null=True)
    sender = models.CharField(_('Sender Number'), max_length=200, blank=True, null=True)
    totalSMSCount = models.IntegerField(_('Total SMS count'), default=0)
    totalFailureCount = models.IntegerField(_('Total Failure count'), default=0)
    totalCost = models.FloatField(_('Total Cost in Tomans'), default=0)

    def __str__(self):
        return self.title
