# Generated by Django 5.0.6 on 2024-05-23 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_questionanswer_is_correct'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cat_quest', to='accounts.category_questions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_result', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]