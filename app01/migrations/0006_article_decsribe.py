# Generated by Django 3.2.2 on 2021-05-10 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='decsribe',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
