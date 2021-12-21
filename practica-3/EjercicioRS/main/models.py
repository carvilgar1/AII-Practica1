from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

class Libro(models.Model):
    titulo = models.TextField(null=True, blank=True)
    autor = models.TextField(null=True, blank=True)
    genero = models.TextField()
    idioma = models.TextField()

    def __str__(self):
        return self.titulo

    
class Rating(models.Model):
    userId = models.PositiveIntegerField(null=True)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, null=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    def __str__(self):
        return str(self.rating)