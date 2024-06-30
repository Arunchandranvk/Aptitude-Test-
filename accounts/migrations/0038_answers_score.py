# Generated by Django 5.0.6 on 2024-06-14 10:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_remove_setofexams_attendedstudentscount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans', models.CharField(max_length=100)),
                ('is_correct', models.BooleanField(null=True)),
                ('cat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cat_quess', to='accounts.category_questions')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ques_ans', to='accounts.questions')),
                ('set', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='set', to='accounts.setofexams')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_ans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField()),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score', to='accounts.setofexams')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='set_score', to='accounts.attendedstudents')),
            ],
        ),
    ]