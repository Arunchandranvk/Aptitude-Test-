# Generated by Django 5.0.6 on 2024-05-23 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_questionanswer_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionanswer',
            name='is_correct',
            field=models.BooleanField(null=True),
        ),
    ]
