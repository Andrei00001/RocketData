# Generated by Django 4.1.3 on 2022-11-06 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0010_alter_products_market_launch_date"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="enterprise",
            index=models.Index(fields=["level"], name="level_idx"),
        ),
    ]
