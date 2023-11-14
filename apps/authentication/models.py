from django.contrib.auth.models import AbstractUser
from apps.sis.models import Sis_Rol
from django.db import models
class AbstractUserModificado(AbstractUser):
    rol = models.ForeignKey(Sis_Rol, models.DO_NOTHING, verbose_name="Rol", default=2)
    class Meta:
        abstract = True

class UserModificado(AbstractUserModificado):

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'