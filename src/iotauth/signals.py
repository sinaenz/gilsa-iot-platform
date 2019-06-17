from random import randint

import kavenegar
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.models import KavenegarConfig

from .models import User


@receiver(post_save, sender=User)
def send_verification_sms(sender, instance, **kwargs):
    # send sms after registration
    if kwargs['created']:
        code = str(randint(1000, 9999))

        instance.is_verified = False
        instance.verification_code = code
        instance.save()
        # send sms
        try:
            api = kavenegar.KavenegarAPI(KavenegarConfig.load().api)
            params = {
                'receptor': instance.phone,
                'message': 'اپلیکیشن مستر اسمارت\nکد شما : {}'.format(code),
            }
            api.sms_send(params)
        except Exception as error:
            print(error)

    # todo: handle resend sms!

