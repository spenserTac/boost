from django.db import models

class UserCreationModel(models.Model):
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    phone = models.CharField(max_length=300)
    password = models

    def __str__(self):
        return (self.first_name + self.last_name + " - " + self.email)