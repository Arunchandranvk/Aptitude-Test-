# Generated by Django 5.0.6 on 2024-05-19 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_questions_correct_ans'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='correct_ans',
            field=models.CharField(choices=[], max_length=100, null=True),
        ),
    ]
