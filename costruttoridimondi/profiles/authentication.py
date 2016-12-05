import sys
from . import models 

class PasswordlessAuthenticationBackend(object):

    def authenticate(self, uid):
        print('uid', uid, file=sys.stderr)
        if not models.Token.objects.filter(uid=uid).exists():
            print('no token found', file=sys.stderr)
            return None
        token = models.Token.objects.get(uid=uid)
        print('got token', file=sys.stderr)
        try:
            user = models.CostruttoriUser.objects.get(email=token.email)
            print('got user', file=sys.stderr)
            return user
        except models.CostruttoriUser.DoesNotExist:
            print('new user', file=sys.stderr)
            return models.CostruttoriUser.objects.create(email=token.email)


    def get_user(self, email):
        return models.CostruttoriUser.objects.get(email=email)
