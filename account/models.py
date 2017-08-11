# from django.db import models
#
#
# # Create your models here.
# class PasswordReset(models.Model):
#
#     user = models.ForeignKey('User', related_name='users')
#     created = models.DateTimeField(auto_now_add=True, auto_now=False)
#     expired = models.DateTimeField(null=True, blank=True)
#     hash =  models.TextField()
#     ativo = models.NullBooleanField()
#
#     def __str__(self):
#         return self.user.username
#
#     class Meta:
#         ordering = ['-id']
#         verbose_name = 'Password Reset'
#         verbose_name_plural = 'Passwords  Reset'
