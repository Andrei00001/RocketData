# Generated by Django 4.1.3 on 2022-11-06 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0011_enterprise_level_enterprise_level_idx"),
    ]

    operations = [
        migrations.AlterField(
            model_name="enterpriseemployees",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="enterprise_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
