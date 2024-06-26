# Generated by Django 5.0.3 on 2024-04-03 19:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Foods",
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
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("果物", "果物"),
                            ("野菜", "野菜"),
                            ("肉", "肉"),
                            ("乳製品", "乳製品"),
                            ("調味料", "調味料"),
                            ("特殊調味料", "特殊調味料"),
                            ("穀物類", "穀物類"),
                            ("インスタント食品", "インスタント食品"),
                            ("お菓子", "お菓子"),
                            ("飲料", "飲料"),
                            ("その他", "その他"),
                        ],
                        default="その他",
                        max_length=100,
                    ),
                ),
                ("expirydate", models.DateField()),
                ("quantity", models.IntegerField()),
            ],
            options={
                "db_table": "foods",
            },
        ),
        migrations.CreateModel(
            name="Pictures",
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
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
                ("picture", models.FileField(upload_to="pictures/")),
                (
                    "food",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pictures",
                        to="food.foods",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
