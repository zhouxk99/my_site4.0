from django.contrib import admin
from app01 import models
# Register your models here.

admin.site.register(models.Account)
admin.site.register(models.Article)
admin.site.register(models.Tag)