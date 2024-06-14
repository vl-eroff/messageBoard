from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    phone = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Trade(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades', blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('open', 'Открыто'), ('closed', 'Закрыто')], default='open')
    title = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.status})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'message': self.message
        }


class Image(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='image_set')
    image = models.FileField(upload_to='trades_images')

    def __str__(self):
        return f"{self.trade.title} - {self.image.name}"