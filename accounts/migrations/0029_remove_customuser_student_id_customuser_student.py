# Generated by Django 5.0.6 on 2024-06-10 06:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_alter_customuser_student_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='student_id',
        ),
        migrations.AddField(
            model_name='customuser',
            name='student',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stu_user', to='accounts.students'),
        ),
    ]
