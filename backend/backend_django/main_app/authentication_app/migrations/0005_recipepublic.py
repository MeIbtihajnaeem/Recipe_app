# Generated by Django 5.1.6 on 2025-02-07 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication_app", "0004_recipe_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecipePublic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("recipe", models.CharField(max_length=200)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
