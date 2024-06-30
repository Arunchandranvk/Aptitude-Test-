from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class CustomUserBackend(BaseBackend):
    def authenticate(self, email=None, password=None):
        try:
            user = CustomUser.objects.get(email=email)
            print(user,'======')
            if user.check_password(password):
                print('----------------')
                return user
        except Exception as e:
            print(e)
