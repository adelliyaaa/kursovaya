from django.contrib import admin

from myapp.models.project import Project
from myapp.models.category import Category
from myapp.models.tag import Tag
from myapp.models.projectimage import ProjectImage
from myapp.models.chat import Chat

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ProjectImage)
admin.site.register(Chat)

