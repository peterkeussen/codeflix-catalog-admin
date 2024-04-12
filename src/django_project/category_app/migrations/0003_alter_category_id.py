# Generated by Django 5.0.4 on 2024-04-11 22:49

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category_app', '0002_alter_category_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True),
        ),
    ]