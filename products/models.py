from django.db import models

class Comic(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='comics/', blank=True, null=True)

    def __str__(self):
        return self.title
