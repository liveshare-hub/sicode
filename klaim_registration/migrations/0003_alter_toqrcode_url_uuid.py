# Generated by Django 3.2.8 on 2021-11-08 11:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('klaim_registration', '0002_auto_20211108_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toqrcode',
            name='url_uuid',
            field=models.UUIDField(default=uuid.UUID('0ef3fca8-0a12-4287-a260-29828121c0c9'), editable=False),
        ),
    ]
