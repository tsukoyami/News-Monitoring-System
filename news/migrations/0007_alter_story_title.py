# Generated by Django 5.0.4 on 2024-04-22 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_alter_story_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='title',
            field=models.CharField(max_length=10000),
        ),
    ]