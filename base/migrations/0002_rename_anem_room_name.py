# Generated by Django 5.0.2 on 2024-03-05 20:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="room",
            old_name="anem",
            new_name="name",
        ),
    ]
