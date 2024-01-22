from django.db import models

from category.models import Category


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=225)
    body = models.TextField(blank=True)
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

    category = models.ForeignKey(Category, related_name='posts', on_delete=models.SET_NULL, null=True)
    preview = models.ImageField(upload_to='images', null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    currency = models.CharField(max_length=3, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.owner} - {self.title[:25]}'


    class Meta:
        ordering = ('created_at',)


class PostImage(models.Model):
    image = models.ImageField(upload_to='images')
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)






