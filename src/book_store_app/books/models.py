from django.db import models

# Create your models here.

class Book(models.Model):
    class Meta:
        db_table = 'book'
    name = models.CharField(max_length=200, null=False, blank=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField()
    stars = models.IntegerField()
    
    def __str__(self):
        return self.name