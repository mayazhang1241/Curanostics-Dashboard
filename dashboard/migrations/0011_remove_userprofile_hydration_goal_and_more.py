# Generated by Django 5.1.5 on 2025-01-28 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0010_alter_passportcategory_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="hydration_goal",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="steps_goal",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="birth_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
