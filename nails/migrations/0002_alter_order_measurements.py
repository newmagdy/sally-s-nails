# Generated by Django 5.1.3 on 2024-12-29 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nails', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='measurements',
            field=models.JSONField(default=list, null=True),
        ),
    ]
