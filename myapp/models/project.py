from django.contrib.auth.models import User
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    link = models.URLField(blank=True)
    category = models.ForeignKey('category', on_delete=models.CASCADE)  # категория
    tags = models.ManyToManyField('tag')  # теги
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"

