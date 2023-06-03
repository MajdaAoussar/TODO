from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser) :
    pass

class Task(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    description = models.CharField(max_length=90)
    time = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description} {self.time}"

