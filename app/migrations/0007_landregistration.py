# Generated by Django 4.1.5 on 2023-03-01 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_landrequest"),
    ]

    operations = [
        migrations.CreateModel(
            name="LandRegistration",
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
                ("buyer_name", models.CharField(max_length=50, null=True)),
                ("buyer_email", models.EmailField(max_length=254)),
                ("buyer_number", models.CharField(max_length=255, null=True)),
                ("total_amount", models.PositiveIntegerField()),
                ("total_land", models.PositiveIntegerField()),
                ("date", models.DateField(auto_now_add=True)),
                (
                    "land",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.landdetails",
                    ),
                ),
                (
                    "seller",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.register"
                    ),
                ),
            ],
        ),
    ]
