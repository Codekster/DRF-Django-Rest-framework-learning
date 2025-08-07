from django.db import models

class Employees(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    salary=models.IntegerField(default=10000)

    def __str__(self):
        return self.name

# Create your models here.
