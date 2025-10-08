from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name        = models.CharField(max_length=155, unique=True)
    slug        = models.SlugField(max_length=155, unique=True)
    description = models.TextField(blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name        = models.CharField(max_length=155, )
    description = models.TextField()
    price       = models.DecimalField(max_digits=5, decimal_places=2, )
    slug        = models.SlugField(max_length=155, unique=True)
    stock       = models.PositiveIntegerField()
    is_active   = models.BooleanField(default=True)
    
    category    = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', )
    
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
