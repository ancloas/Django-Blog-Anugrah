# Generated by Django 5.0 on 2023-12-14 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='name',
            field=models.TextField(null=True),
        ),
    ]