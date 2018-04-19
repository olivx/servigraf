from django.db import models
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, force_bytes
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
def path_avatar(instance, filename):
    path ='avatar/'
    ext = filename.split('.')[-1]
    file_name  = '%s.%s' % (urlsafe_base64_encode(force_bytes(instance.user.pk)), ext)
    return os.path.join(path, file_name)

class Profile(models.Model):

    CLIENT_USER = 1
    NORMAL_USER = 2
    ADMIN_USER = 3
    KINDS =[
        (CLIENT_USER, 'Cliente'),
        (NORMAL_USER, 'Comum'),
        (ADMIN_USER, 'Admin')
    ]

    user =  models.OneToOneField(User, primary_key=True)
    type = models.PositiveIntegerField('Tipo', choices=KINDS, default=NORMAL_USER)
    full_name =  models.CharField('Nome Completo', max_length=255,blank=True, null=True)
    avatar =  models.ImageField('Avatar', upload_to=path_avatar, blank=True, null=True)
    birdayth = models.DateField(null=True, blank=True)


    def __str__(sefl):
        return self.full_name

    class Meta:
        verbose_name =  'Profile'
        verbose_name_plural = 'Profiles'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    profile, created = Profile.objects.get_or_create(user=instance)
    profile.full_name = instance.get_full_name()
    profile.save()
