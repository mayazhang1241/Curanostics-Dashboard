# Generated by Django 5.1.5 on 2025-01-28 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0008_alter_exerciselog_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exerciselog",
            options={"ordering": ["-date"]},
        ),
        migrations.AlterModelOptions(
            name="hydrationlog",
            options={"ordering": ["-date"]},
        ),
        migrations.AddField(
            model_name="exerciselog",
            name="calories_burned",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="exerciselog",
            name="duration_minutes",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="hydrationlog",
            name="goal",
            field=models.FloatField(default=64.0),
        ),
    ]
