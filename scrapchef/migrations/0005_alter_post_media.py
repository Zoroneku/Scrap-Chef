# Generated by Django 5.1.7 on 2025-03-25 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scrapchef", "0004_alter_post_media"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="Media",
            field=models.ImageField(upload_to="uploads/"),
        ),
    ]
