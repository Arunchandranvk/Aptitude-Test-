# Generated by Django 5.0.6 on 2024-05-22 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_questionanswer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.CharField(max_length=200)),
            ],
        ),
    ]
