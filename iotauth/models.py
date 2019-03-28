from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from random import randint
import kavenegar
from utils.models import KavenegarConfig
import uuid


# ===========================================================================
# ============================== User Manager ===============================
# ===========================================================================
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone and password.
        """
        if not phone:
            raise ValueError('Users must have a phone number!')

        user = self.model(
            phone=phone,
        )
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        """
        Creates and saves a superuser with the given phone and password.
        """
        user = self.create_user(
            phone=phone,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def verified_users(self):
        return self.get_queryset().filter(is_verified=True)


# ===========================================================================
# =============================== User Model ================================
# ===========================================================================
class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    # user data
    phone = models.CharField(_('phone'), max_length=40, unique=True, blank=True, null=True)
    full_name = models.CharField(_('full name'), max_length=40, blank=True, null=True)
    uuid = models.UUIDField(_('user unique id'), default=uuid.uuid4, unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    # avatar
    avatar = models.ImageField('Avatar', upload_to='avatar/%Y/%m/%d', default='avatar/avatar.png')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    # registration
    verification_code = models.CharField(_('Verification Code'), max_length=120, blank=True, null=True)
    is_verified = models.BooleanField('is verified?', default=False)

    def image_tag(self):
        img = '/media/avatar/avatar.png'
        if hasattr(self, 'avatar'):
            try:
                img = self.avatar.url
            except:
                pass
        return mark_safe('<img src="{}" style="width: 50px; height:50px; border-radius:25px;"/>'.format(img))

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def send_verification_sms(self):
        code = str(randint(1000, 9999))

        self.is_verified = False
        self.verification_code = code
        self.save()
        # send sms async
        try:
            api = kavenegar.KavenegarAPI(KavenegarConfig.load().api)
            params = {
                'receptor': self.phone,
                'message': 'اپلیکیشن مستر اسمارت\nکد شما : {}'.format(code),
                'sender': KavenegarConfig.load().sender
            }
            api.sms_send(params)
        # TODO: should raise appropriate exception
        except:
            pass

    def __str__(self):
        return self.full_name
