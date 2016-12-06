from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordlessAuthenticationBackend(object):

    def authenticate(self, uid):
        try:
            token=models.Token.objects.get(uid=uid)
            user=User.objects.get(email=token.email)
        except User.DoesNotExist:
            user=User.objects.create(email=token.email)
        except models.Token.DoesNotExist:
            return None
        return user

    def get_user(self,email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
