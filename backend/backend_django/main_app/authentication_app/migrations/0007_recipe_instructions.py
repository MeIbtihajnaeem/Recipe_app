# Generated by Django 5.1.6 on 2025-02-07 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication_app", "0006_ingredientspublic"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="instructions",
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
