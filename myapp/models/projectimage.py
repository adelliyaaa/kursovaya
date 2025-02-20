from django.db import models

from myapp.models.project import Project


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return self.project.title

    class Meta:
        ordering = ['image']
        verbose_name = 'Image'
        verbose_name_plural = 'Images'