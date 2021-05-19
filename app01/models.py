from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# class Account(models.Model):
class Account(models.Model):

    """账户表"""
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    register_date = models.DateTimeField(auto_now_add=True)
    signature = models.CharField("签名", max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

class Tag(models.Model):
    """标签"""
    name = models.CharField(max_length=64, unique=True)
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    """文章表"""
    title = models.CharField(max_length=255, unique=True)
    decsribe = models.TextField()
    content = models.TextField()
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    tags = models.ForeignKey("Tag", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class ArticleUpdown(models.Model):
    """
    点赞
    """
    nid = models.AutoField(primary_key = True)
    user = models.ForeignKey('Account', null = True, on_delete=models.CASCADE)
    article = models.ForeignKey("Article", null = True, on_delete=models.CASCADE)
    is_up = models.BooleanField(default = True)    # 点赞 or 点踩

    class Meta:
        unique_together = [
            ('article', 'user')
        ]

class Comment(models.Model):
    """
    评论
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey("Account", on_delete=models.CASCADE)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    parent_comment = models.ForeignKey('self', null = True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content