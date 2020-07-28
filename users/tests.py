from django.test import TestCase

# Create your tests here.
from users.models import Users

u = Users.objects.get(username="liuxiang")
print(u.token)