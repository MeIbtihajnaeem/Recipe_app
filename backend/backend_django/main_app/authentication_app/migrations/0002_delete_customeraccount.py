# Generated by Django 5.1.6 on 2025-02-07 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentication_app", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CustomerAccount",
        ),
    ]
